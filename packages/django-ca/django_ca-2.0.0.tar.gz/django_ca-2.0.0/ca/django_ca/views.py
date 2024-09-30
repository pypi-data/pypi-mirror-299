# This file is part of django-ca (https://github.com/mathiasertl/django-ca).
#
# django-ca is free software: you can redistribute it and/or modify it under the terms of the GNU General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# django-ca is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License along with django-ca. If not, see
# <http://www.gnu.org/licenses/>.

"""Views for the django-ca app.

.. seealso::

   * https://docs.djangoproject.com/en/dev/topics/class-based-views/
   * https://django-ca.readthedocs.io/en/latest/python/views.html
"""

import base64
import binascii
import logging
import typing
import warnings
from datetime import datetime, timedelta, timezone as tz
from http import HTTPStatus
from typing import Any, Optional, Union, cast

from pydantic import BaseModel

from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.types import CertificateIssuerPrivateKeyTypes
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography.x509 import (
    ExtensionNotFound,
    OCSPNonce,
    load_der_x509_certificate,
    load_pem_x509_certificate,
    ocsp,
)

from django.core.cache import cache
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin

from django_ca import constants
from django_ca.constants import CERTIFICATE_REVOCATION_LIST_ENCODING_TYPES
from django_ca.deprecation import RemovedInDjangoCA210Warning
from django_ca.models import Certificate, CertificateAuthority
from django_ca.typehints import CertificateRevocationListEncodings
from django_ca.utils import SERIAL_RE, get_crl_cache_key, int_to_hex, parse_encoding, read_file

log = logging.getLogger(__name__)

if typing.TYPE_CHECKING:
    from django.http.response import HttpResponseBase

    SingleObjectMixinBase = SingleObjectMixin[CertificateAuthority]
else:
    SingleObjectMixinBase = SingleObjectMixin


class CertificateRevocationListView(View, SingleObjectMixinBase):
    """Generic view that provides Certificate Revocation Lists (CRLs)."""

    slug_field = "serial"
    slug_url_kwarg = "serial"
    queryset = CertificateAuthority.objects.all().prefetch_related("certificate_set")

    password = None
    """Password used to load the private key of the certificate authority. If not set, the private key is
    assumed to be unencrypted."""

    # parameters for the CRL itself
    type: CertificateRevocationListEncodings = Encoding.DER
    """Encoding for CRL."""

    scope: Optional[typing.Literal["ca", "user", "attribute"]] = "user"
    """Set to ``"user"`` to limit CRL to certificates or ``"ca"`` to certificate authorities or ``None`` to
    include both."""

    expires = 600
    """CRL expires in this many seconds."""

    # header used in the request
    content_type = None
    """Value of the Content-Type header used in the response. For CRLs in PEM format, use ``text/plain``."""

    include_issuing_distribution_point: Optional[bool] = None
    """Boolean flag to force inclusion/exclusion of IssuingDistributionPoint extension."""

    def get_key_backend_options(self, ca: CertificateAuthority) -> BaseModel:
        """Method to get the key backend options to access the private key.

        If a custom CA backend needs transient parameters (e.g. passwords), a view overriding this method
        must be implemented.
        """
        if self.password is not None:  # pragma: no cover
            warnings.warn(
                "Configuring a password in views is deprecated, use the CA_PASSWORDS setting instead.",
                RemovedInDjangoCA210Warning,
                stacklevel=2,
            )
        return ca.key_backend.get_use_private_key_options(ca, {"password": self.password})

    def fetch_crl(self, ca: CertificateAuthority, encoding: CertificateRevocationListEncodings) -> bytes:
        """Actually fetch the CRL (nested function so that we can easily catch any exception)."""
        cache_key = get_crl_cache_key(ca.serial, encoding=encoding, scope=self.scope)

        encoded_crl: Optional[bytes] = cache.get(cache_key)
        if encoded_crl is None:
            # Catch this case early so that we can give a better error message
            if self.include_issuing_distribution_point is True and ca.parent is None and self.scope is None:
                raise ValueError(
                    "Cannot add IssuingDistributionPoint extension to CRLs with no scope for root CAs."
                )

            key_backend_options = self.get_key_backend_options(ca)
            crl = ca.get_crl(
                key_backend_options,
                expires=self.expires,
                scope=self.scope,
                include_issuing_distribution_point=self.include_issuing_distribution_point,
            )
            encoded_crl = crl.public_bytes(encoding)
            cache.set(cache_key, encoded_crl, self.expires)
        return encoded_crl

    def get(self, request: HttpRequest, serial: str) -> HttpResponse:  # pylint: disable=unused-argument
        # pylint: disable=missing-function-docstring; standard Django view function
        if get_encoding := request.GET.get("encoding"):
            if get_encoding not in CERTIFICATE_REVOCATION_LIST_ENCODING_TYPES:
                return HttpResponseBadRequest(
                    f"{get_encoding}: Invalid encoding requested.", content_type="text/plain"
                )
            # TYPEHINT NOTE: type is verified in the previous line
            encoding = cast(CertificateRevocationListEncodings, parse_encoding(get_encoding))
        else:
            encoding = self.type

        ca = self.get_object()
        try:
            crl = self.fetch_crl(ca, encoding)
        except Exception:  # pylint: disable=broad-exception-caught
            log.exception("Error generating a CRL")
            return HttpResponseServerError("Error while retrieving the CRL.", content_type="text/plain")

        content_type = self.content_type
        if content_type is None:
            if encoding == Encoding.DER:
                content_type = "application/pkix-crl"
            elif encoding == Encoding.PEM:
                content_type = "text/plain"
            else:  # pragma: no cover
                # DER/PEM are all known encoding types, so this shouldn't happen
                return HttpResponseServerError()

        return HttpResponse(crl, content_type=content_type)


@method_decorator(csrf_exempt, name="dispatch")
class OCSPView(View):
    """View to provide an OCSP responder."""

    ca: str = ""
    """The name or serial of your Certificate Authority."""

    responder_key: str = ""
    """Private key used for signing OCSP responses. A relative path used by :ref:`CA_FILE_STORAGE
    <settings-ca-file-storage>`."""

    responder_cert: Union[x509.Certificate, str] = ""
    """Public key of the responder.

    This may either be:

    * A relative path used by :ref:`CA_FILE_STORAGE <settings-ca-file-storage>`
    * A serial of a certificate as stored in the database
    * The PEM of the certificate as string
    * A loaded :py:class:`~cg:cryptography.x509.Certificate`
    """

    expires = 600
    """Time in seconds that the responses remain valid. The default is 600 seconds or ten minutes."""

    ca_ocsp = False
    """If set to ``True``, validate child CAs instead."""

    def get(self, request: HttpRequest, data: str) -> HttpResponse:
        # pylint: disable=missing-function-docstring; standard Django view function
        try:
            decoded_data = base64.b64decode(data)
        except binascii.Error:
            return self.malformed_request()

        try:
            return self.process_ocsp_request(decoded_data)
        except Exception as e:  # pylint: disable=broad-except; we really need to catch everything here
            log.exception(e)
            return self.fail()

    def post(self, request: HttpRequest) -> HttpResponse:
        # pylint: disable=missing-function-docstring; standard Django view function
        try:
            return self.process_ocsp_request(request.body)
        except Exception as e:  # pylint: disable=broad-except; we really need to catch everything here
            log.exception(e)
            return self.fail()

    def fail(self, status: ocsp.OCSPResponseStatus = ocsp.OCSPResponseStatus.INTERNAL_ERROR) -> HttpResponse:
        """Generic method to return a failure response."""
        return self.http_response(
            ocsp.OCSPResponseBuilder.build_unsuccessful(status).public_bytes(Encoding.DER)
        )

    def get_responder_key(self) -> CertificateIssuerPrivateKeyTypes:
        """Get the private key used to sign OCSP responses."""
        key = self.get_responder_key_data()

        try:
            loaded_key = serialization.load_der_private_key(key, None)
        except ValueError:
            try:
                loaded_key = serialization.load_pem_private_key(key, None)
            except ValueError as ex:
                raise ValueError("Could not decrypt private key.") from ex

        # Check that the private key is of a supported type
        if not isinstance(loaded_key, constants.PRIVATE_KEY_TYPES):
            log.error("%s: Unsupported private key type.", type(loaded_key))
            raise ValueError(f"{type(loaded_key)}: Unsupported private key type.")

        return loaded_key  # type: ignore[return-value]  # mypy not smart enough for above isinstance() check

    def get_responder_key_data(self) -> bytes:
        """Read the file containing the private key used to sign OCSP responses."""
        return read_file(self.responder_key)

    def get_responder_cert(self) -> x509.Certificate:
        """Get the public key used to sign OCSP responses."""
        # User configured a loaded certificate
        if isinstance(self.responder_cert, x509.Certificate):
            return self.responder_cert

        if self.responder_cert.startswith("-----BEGIN CERTIFICATE-----\n"):
            responder_cert = self.responder_cert.encode("utf-8")
        elif SERIAL_RE.match(self.responder_cert):
            serial = self.responder_cert.replace(":", "")
            return Certificate.objects.get(serial=serial).pub.loaded
        else:
            responder_cert = read_file(self.responder_cert)

        try:
            return load_der_x509_certificate(responder_cert)
        except ValueError:
            return load_pem_x509_certificate(responder_cert)

    def get_ca(self) -> CertificateAuthority:
        """Get the certificate authority for the request."""
        return CertificateAuthority.objects.get_by_serial_or_cn(self.ca)

    def get_cert(self, ca: CertificateAuthority, serial: str) -> Union[Certificate, CertificateAuthority]:
        """Get the certificate that was requested in the OCSP request."""
        if self.ca_ocsp is True:
            return CertificateAuthority.objects.filter(parent=ca).get(serial=serial)

        return Certificate.objects.filter(ca=ca).get(serial=serial)

    def get_expires(self, now: datetime) -> datetime:
        """Get the timestamp when the OCSP response expires."""
        return now + timedelta(seconds=self.expires)

    def http_response(self, data: bytes, status: int = HTTPStatus.OK) -> HttpResponse:
        """Get an HTTP OCSP response with given status and data."""
        return HttpResponse(data, status=status, content_type="application/ocsp-response")

    def malformed_request(self) -> HttpResponse:
        """Get a response for a malformed request."""
        return self.fail(ocsp.OCSPResponseStatus.MALFORMED_REQUEST)

    def process_ocsp_request(self, data: bytes) -> HttpResponse:
        """Process OCSP request data."""
        try:
            ocsp_req = ocsp.load_der_ocsp_request(data)
        except Exception as e:  # pylint: disable=broad-except; we really need to catch everything here
            log.exception(e)
            return self.malformed_request()

        # Fail if there are any critical extensions that we do not understand
        for ext in ocsp_req.extensions:
            if ext.critical and not isinstance(ext.value, OCSPNonce):  # pragma: no cover
                # It seems impossible to get cryptography to create such a request, so it's not tested
                return self.malformed_request()

        # Get CA and certificate
        try:
            ca = self.get_ca()
        except CertificateAuthority.DoesNotExist:
            log.error("%s: Certificate Authority could not be found.", self.ca)
            return self.fail()

        cert_serial = int_to_hex(ocsp_req.serial_number)

        # NOINSPECTION NOTE: PyCharm wrongly things that second except is already covered by the first.
        # noinspection PyExceptClausesOrder
        try:
            cert = self.get_cert(ca, cert_serial)
        except CertificateAuthority.DoesNotExist:
            log.warning("%s: OCSP request for unknown CA received.", cert_serial)
            return self.fail()
        except Certificate.DoesNotExist:
            log.warning("%s: OCSP request for unknown cert received.", cert_serial)
            return self.fail()

        # get key/cert for OCSP responder
        try:
            responder_key = self.get_responder_key()
            responder_cert = self.get_responder_cert()
        except Exception:  # pylint: disable=broad-except; we really need to catch everything here
            log.error("Could not read responder key/cert.")
            return self.fail()

        # get the certificate status
        if cert.revoked:
            status = ocsp.OCSPCertStatus.REVOKED
        else:
            status = ocsp.OCSPCertStatus.GOOD

        now = datetime.now(tz=tz.utc)
        builder = ocsp.OCSPResponseBuilder()
        expires = self.get_expires(now)
        builder = builder.add_response(
            cert=cert.pub.loaded,
            issuer=ca.pub.loaded,
            # The algorithm used must be the same as in the request, or "openssl ocsp" won't be able to
            # determine the status (verified: NOT the hash algorithm of the requested certificate).
            algorithm=ocsp_req.hash_algorithm,
            cert_status=status,
            this_update=now.replace(tzinfo=None),
            next_update=expires,
            revocation_time=cert.get_revocation_time(),
            revocation_reason=cert.get_revocation_reason(),
        ).responder_id(ocsp.OCSPResponderEncoding.HASH, responder_cert)

        # Add the responder/delegate certificate to the response
        builder = builder.certificates([responder_cert])

        # Add OCSP nonce if present
        try:
            nonce = ocsp_req.extensions.get_extension_for_class(OCSPNonce)
            builder = builder.add_extension(nonce.value, critical=nonce.critical)
        except ExtensionNotFound:
            pass

        # The hash algorithm may be different from the signature hash algorithm of the responder certificate,
        # but must be None for Ed448/Ed25519 certificates. Since delegate certificates are ephemeral anyway,
        # configuring the hash algorithm is not supported, instead the user is expected to generate new keys
        # with a different private key type or hash algorithm if desired.
        response = builder.sign(responder_key, responder_cert.signature_hash_algorithm)

        return self.http_response(response.public_bytes(Encoding.DER))


@method_decorator(csrf_exempt, name="dispatch")
class GenericOCSPView(OCSPView):
    """View providing auto-configured OCSP functionality.

    This view assumes that ``ocsp/$ca_serial.(key|pem)`` point to the private/public key of a responder
    certificate as created by :py:class:`~django_ca.tasks.generate_ocsp_keys`. The ``serial`` URL keyword
    argument must be the serial for this CA.
    """

    auto_ca: CertificateAuthority

    # NOINSPECTION NOTE: It's okay to be more specific here
    # noinspection PyMethodOverriding
    def dispatch(self, request: HttpRequest, serial: str, **kwargs: Any) -> "HttpResponseBase":
        if request.method == "GET" and "data" not in kwargs:
            return self.http_method_not_allowed(request, serial, **kwargs)
        if request.method == "POST" and "data" in kwargs:
            return self.http_method_not_allowed(request, serial, **kwargs)

        # COVERAGE NOTE: Checking just for safety here.
        if not isinstance(serial, str):  # pragma: no cover
            raise ImproperlyConfigured("View expects a str for a serial")

        self.auto_ca = CertificateAuthority.objects.get(serial=serial)
        return super().dispatch(request, **kwargs)

    def get_ca(self) -> CertificateAuthority:
        return self.auto_ca

    def get_expires(self, now: datetime) -> datetime:
        return now + timedelta(seconds=self.auto_ca.ocsp_response_validity)

    def get_responder_key_data(self) -> bytes:
        serial = self.auto_ca.serial.replace(":", "")
        return read_file(f"ocsp/{serial}.key")

    def get_responder_cert(self) -> x509.Certificate:
        return self.auto_ca.ocsp_responder_certificate


class GenericCAIssuersView(View):
    """Generic view that returns a CA public key in DER format.

    This view serves the URL named in the ``issuers`` key in the
    :py:class:`~cg:cryptography.x509.AuthorityInformationAccess` extension.
    """

    def get(self, request: HttpRequest, serial: str) -> HttpResponse:
        # pylint: disable=missing-function-docstring; standard Django view function
        ca = CertificateAuthority.objects.get(serial=serial)
        return HttpResponse(ca.pub.der, content_type="application/pkix-cert")

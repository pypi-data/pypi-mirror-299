# Generated by Django 3.2 on 2021-04-29 00:00

from cryptography import x509

from django.db import migrations


def migrate(apps, schema_editor):
    Certificate = apps.get_model("django_ca", "Certificate")
    CertificateAuthority = apps.get_model("django_ca", "CertificateAuthority")

    for cert in Certificate.objects.all():
        if cert.csr != "":
            try:
                csr = x509.load_pem_x509_csr(cert.csr.encode())
            except Exception:
                print(f"{cert}: Could not convert CSR.")
                continue
            cert.csr_tmp = csr

        try:
            cert.pub_tmp = x509.load_pem_x509_certificate(cert.pub.encode())
        except Exception:
            print(f"{cert}: Could not convert PEM.")
            continue
        cert.save()

    for ca in CertificateAuthority.objects.all():
        try:
            ca.pub_tmp = x509.load_pem_x509_certificate(ca.pub.encode())
        except Exception:
            print(f"{ca}: Could not convert PEM.")
            continue
        ca.save()


def noop(apps, schema_editor):
    """no need to do anything in backwards data migration."""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("django_ca", "0022_auto_20210430_1124"),
    ]

    operations = [
        migrations.RunPython(migrate, noop),
    ]

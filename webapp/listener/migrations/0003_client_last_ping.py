# Generated by Django 4.0.4 on 2022-07-31 17:37

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    """I didn't make this"""

    dependencies = [
        ('listener', '0002_rename_ip_address_client_ip'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='last_ping',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
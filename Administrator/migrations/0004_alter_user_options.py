# Generated by Django 4.2.1 on 2023-06-19 07:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Administrator', '0003_alter_user_is_active'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'managed': False},
        ),
    ]

# Generated by Django 4.0 on 2021-12-25 13:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_rename_id_cart_key_cart_temp_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='key',
            new_name='id',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='temp_id',
        ),
    ]

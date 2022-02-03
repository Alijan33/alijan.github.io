# Generated by Django 4.0 on 2021-12-25 13:27

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_remove_cart_temp_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='id',
            new_name='key',
        ),
        migrations.AddField(
            model_name='cart',
            name='temp_id',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]
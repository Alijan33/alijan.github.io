# Generated by Django 4.0 on 2021-12-25 13:25

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_alter_customer_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='temp_id',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]
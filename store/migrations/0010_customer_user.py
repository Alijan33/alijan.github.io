# Generated by Django 4.0 on 2021-12-24 00:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('store', '0009_remove_customer_email_remove_customer_frist_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='user',
            field=models.OneToOneField(default='0000000', on_delete=django.db.models.deletion.CASCADE, to='core.user'),
        ),
    ]

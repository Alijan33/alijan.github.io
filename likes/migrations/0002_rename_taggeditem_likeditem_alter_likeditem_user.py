# Generated by Django 4.0 on 2021-12-22 12:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('likes', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TaggedItem',
            new_name='LikedItem',
        ),
        migrations.AlterField(
            model_name='likeditem',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.user'),
        ),
    ]

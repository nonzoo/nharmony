# Generated by Django 4.2.4 on 2023-12-16 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0009_alter_postattachment_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postattachment',
            name='image',
            field=models.ImageField(upload_to='post_attachments/<django.db.models.query_utils.DeferredAttribute object at 0x000002E9BAB2FE50>'),
        ),
    ]
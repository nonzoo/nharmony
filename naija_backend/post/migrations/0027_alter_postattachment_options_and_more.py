# Generated by Django 4.2.4 on 2024-01-02 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0026_alter_postattachment_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='postattachment',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AddField(
            model_name='postattachment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]

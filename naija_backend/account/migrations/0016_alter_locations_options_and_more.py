# Generated by Django 4.2.4 on 2024-01-31 08:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0015_user_categories_user_locations'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='locations',
            options={'verbose_name_plural': 'Location'},
        ),
        migrations.RenameField(
            model_name='categories',
            old_name='category',
            new_name='body',
        ),
        migrations.RenameField(
            model_name='locations',
            old_name='location',
            new_name='category',
        ),
    ]

# Generated by Django 4.2.4 on 2024-01-31 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0016_alter_locations_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='locations',
            name='body_test',
            field=models.CharField(max_length=200, null=True),
        ),
    ]

# Generated by Django 4.2.4 on 2024-02-18 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0028_user_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='age_preference',
            field=models.PositiveBigIntegerField(null=True),
        ),
    ]

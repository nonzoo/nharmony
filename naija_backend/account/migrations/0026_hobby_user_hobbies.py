# Generated by Django 4.2.4 on 2024-02-10 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0025_alter_user_locations'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hobby',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': 'Hobby',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='hobbies',
            field=models.ManyToManyField(to='account.hobby'),
        ),
    ]

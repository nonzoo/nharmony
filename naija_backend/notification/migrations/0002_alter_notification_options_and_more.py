# Generated by Django 4.2.4 on 2024-01-30 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notification',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AlterField(
            model_name='notification',
            name='type_of_notification',
            field=models.CharField(choices=[('new_friendrequest', 'New friendrequest'), ('accepted_friendrequest', 'Accepted friendrequest'), ('rejected_friendrequest', 'Rejected friendrequest'), ('post_like', 'Post like'), ('post_comment', 'Post comment')], max_length=50),
        ),
    ]

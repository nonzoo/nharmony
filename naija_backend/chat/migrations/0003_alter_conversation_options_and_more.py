# Generated by Django 4.2.4 on 2023-12-23 14:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_alter_conversation_id_alter_conversationmessage_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='conversation',
            options={'ordering': ('-modified_at_formatted',)},
        ),
        migrations.RenameField(
            model_name='conversation',
            old_name='modified_at',
            new_name='modified_at_formatted',
        ),
    ]

# Generated by Django 5.0.1 on 2024-02-25 18:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_recipent_group_message'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Recipent_Group',
            new_name='Recipient_Group',
        ),
    ]
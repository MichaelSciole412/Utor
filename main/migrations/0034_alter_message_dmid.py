# Generated by Django 5.0.1 on 2024-04-16 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0033_recipient_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='dmid',
            field=models.CharField(max_length=100),
        ),
    ]

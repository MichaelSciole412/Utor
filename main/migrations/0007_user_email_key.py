# Generated by Django 5.0.1 on 2024-02-04 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_user_is_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email_key',
            field=models.CharField(default='helloworld', max_length=50),
            preserve_default=False,
        ),
    ]

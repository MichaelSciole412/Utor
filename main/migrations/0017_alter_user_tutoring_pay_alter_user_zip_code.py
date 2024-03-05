# Generated by Django 5.0.1 on 2024-02-21 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_merge_0012_notification_0015_merge_20240217_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='tutoring_pay',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='zip_code',
            field=models.IntegerField(default=28607, null=True),
        ),
    ]
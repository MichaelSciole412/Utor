# Generated by Django 5.0.1 on 2024-01-23 22:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('domains', models.TextField(null=True)),
                ('web_pages', models.TextField(null=True)),
                ('country', models.CharField(max_length=50)),
                ('alpha_two_code', models.CharField(max_length=10)),
                ('state_province', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.TextField(default="This user hasn't set their bio"),
        ),
        migrations.AddField(
            model_name='user',
            name='university',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='main.university'),
        ),
    ]

# Generated by Django 5.0.1 on 2024-02-15 23:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_alter_studygroup_university'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('n_type', models.CharField(max_length=10)),
                ('title', models.CharField(max_length=150)),
                ('text', models.CharField(max_length=500)),
                ('regarding_group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='gnot_set', to='main.studygroup')),
                ('regarding_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='regu_set', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

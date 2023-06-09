# Generated by Django 4.1.7 on 2023-03-16 09:14

import applications.common.models
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='JsonConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='uuid')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='updated_time')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='created_time')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Name')),
                ('config', models.JSONField(verbose_name='Config')),
                ('min_client_version', models.PositiveIntegerField(default=0, verbose_name='Minimum client version')),
                ('max_client_version', models.PositiveIntegerField(default=1, verbose_name='Maximum client version')),
            ],
            options={
                'verbose_name': 'Json Config',
                'verbose_name_plural': 'Json Configs',
            },
        ),
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='uuid')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='updated_time')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='created_time')),
                ('app_name', models.CharField(default=applications.common.models.get_app_name, max_length=255, verbose_name='app name')),
                ('version', models.CharField(default=applications.common.models.get_version, max_length=255, verbose_name='version')),
                ('social_media_link', models.CharField(blank=True, max_length=255, null=True, verbose_name='social media link')),
                ('deep_link_prefix', models.CharField(blank=True, default='', max_length=255, verbose_name='Deep link prefix')),
                ('maintenance_mode', models.BooleanField(default=False, max_length=255, verbose_name='maintenance mode')),
                ('bypass_verification_email', models.BooleanField(default=False, verbose_name='bypass verification email')),
                ('config', models.ManyToManyField(blank=True, to='common.jsonconfig', verbose_name='config')),
            ],
            options={
                'verbose_name': 'Configuration',
                'verbose_name_plural': 'Configurations',
            },
        ),
    ]

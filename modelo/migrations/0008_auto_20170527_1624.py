# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-27 19:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('modelo', '0007_cliente_max_pontos'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='login',
            field=models.CharField(max_length=45, null=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='senha',
            field=models.CharField(max_length=45, null=True),
        ),
    ]
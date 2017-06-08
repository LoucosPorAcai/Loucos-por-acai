# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-06 21:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelo', '0009_auto_20170530_1626'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='atendimento',
            name='data',
        ),
        migrations.RemoveField(
            model_name='atendimento',
            name='hora',
        ),
        migrations.RemoveField(
            model_name='atendimento',
            name='tipo_entrega',
        ),
        migrations.RemoveField(
            model_name='carrinho',
            name='estoque',
        ),
        migrations.AddField(
            model_name='carrinho',
            name='estoque',
            field=models.ManyToManyField(blank=True, to='modelo.Estoque'),
        ),
        migrations.AlterField(
            model_name='estoque',
            name='quant_produtos',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='cpf',
            field=models.CharField(max_length=14, unique=True),
        ),
    ]
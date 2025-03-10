# Generated by Django 5.1 on 2025-02-04 21:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ciudadano_app', '0010_ciudadano_sector_ciudadano_sectores_de_interes_and_more'),
        ('shared', '0008_alter_sector_estado_alter_sector_nombre'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ciudadano',
            name='sector',
        ),
        migrations.RemoveField(
            model_name='ciudadano',
            name='ubicacion_actual',
        ),
        migrations.AddField(
            model_name='ciudadano',
            name='sector_actual',
            field=models.ForeignKey(blank=True, help_text='Sector donde se encuentra actualmente el ciudadano', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ciudadanos_presentes', to='shared.sector', verbose_name='Sector Actual'),
        ),
        migrations.AlterField(
            model_name='ciudadano',
            name='sectores_de_interes',
            field=models.ManyToManyField(blank=True, help_text='Sectores en los que el ciudadano está interesado', related_name='ciudadanos_interesados', to='shared.sector', verbose_name='Sectores de Interés'),
        ),
    ]

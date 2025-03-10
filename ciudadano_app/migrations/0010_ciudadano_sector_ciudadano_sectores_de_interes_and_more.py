# Generated by Django 5.1.5 on 2025-02-03 06:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ciudadano_app', '0009_remove_ciudadano_groups_and_more'),
        ('shared', '0004_sector_alter_reporte_ciudadano_notificacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='ciudadano',
            name='sector',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shared.sector', verbose_name='Sector'),
        ),
        migrations.AddField(
            model_name='ciudadano',
            name='sectores_de_interes',
            field=models.ManyToManyField(blank=True, related_name='ciudadanos_interesados', to='shared.sector'),
        ),
        migrations.AddField(
            model_name='ciudadano',
            name='ubicacion_actual',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ciudadanos_presentes', to='shared.sector'),
        ),
    ]

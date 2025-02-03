# Generated by Django 5.1.5 on 2025-02-03 06:09

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entidad_municipal_app', '0018_eventomunicipal_entidad_municipal'),
    ]

    operations = [
        migrations.AddField(
            model_name='espaciopublico',
            name='descripcion',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='espaciopublico',
            name='direccion',
            field=models.CharField(help_text='Ubicación donde se encuentra el espacio público', max_length=255, verbose_name='Lugar'),
        ),
        migrations.AlterField(
            model_name='espaciopublico',
            name='entidad_municipal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='espacios_publicos', to='entidad_municipal_app.entidadmunicipal', verbose_name='Entidad Municipal'),
        ),
        migrations.AlterField(
            model_name='espaciopublico',
            name='nombre',
            field=models.CharField(default='Espacio Público', help_text='Nombre del espacio público', max_length=255),
        ),
    ]

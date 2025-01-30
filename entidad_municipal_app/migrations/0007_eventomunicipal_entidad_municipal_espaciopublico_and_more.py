# Generated by Django 5.1 on 2025-01-30 03:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entidad_municipal_app', '0006_canalinformativo_noticia_comentario_reaccion_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventomunicipal',
            name='entidad_municipal',
            field=models.ForeignKey(blank=True, help_text='Entidad municipal a la que pertenece el espacio público', null=True, on_delete=django.db.models.deletion.CASCADE, to='entidad_municipal_app.entidadmunicipal'),
        ),
        migrations.CreateModel(
            name='EspacioPublico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default='Espacio Público', help_text='Nombre del espacio público', max_length=100)),
                ('direccion', models.CharField(default='Dirección no especificada', help_text='Dirección del espacio público', max_length=200)),
                ('disponibilidad', models.BooleanField(default=True)),
                ('entidad_municipal', models.ForeignKey(help_text='Entidad municipal a la que pertenece el espacio público', on_delete=django.db.models.deletion.CASCADE, related_name='espacios_publicos', to='entidad_municipal_app.entidadmunicipal')),
            ],
            options={
                'verbose_name': 'Espacio Público',
                'verbose_name_plural': 'Espacios Públicos',
            },
        ),
        migrations.AddField(
            model_name='eventomunicipal',
            name='lugar_evento',
            field=models.ForeignKey(blank=True, help_text='Ubicación donde se realizará el evento', null=True, on_delete=django.db.models.deletion.CASCADE, to='entidad_municipal_app.espaciopublico'),
        ),
    ]

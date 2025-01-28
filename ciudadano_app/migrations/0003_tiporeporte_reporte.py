# Generated by Django 5.1 on 2025-01-27 04:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ciudadano_app', '0002_reserva'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoReporte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asunto', models.CharField(max_length=200)),
                ('descripcion', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Reporte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ubicacion', models.CharField(max_length=255)),
                ('prioridad', models.IntegerField(blank=True, default=None, null=True)),
                ('ciudadano', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tipo_reporte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ciudadano_app.tiporeporte')),
            ],
        ),
    ]

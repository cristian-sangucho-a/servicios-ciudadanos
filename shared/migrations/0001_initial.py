# Generated by Django 5.1 on 2025-01-30 02:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('entidad_municipal_app', '0008_reportemunicipal'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoReporte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asunto', models.CharField(max_length=200)),
                ('descripcion', models.TextField()),
                ('prioridad_de_atencion', models.IntegerField(default=0)),
                ('departamento', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='entidad_municipal_app.departamento')),
            ],
        ),
        migrations.CreateModel(
            name='Reporte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ubicacion', models.CharField(max_length=255)),
                ('prioridad', models.IntegerField(blank=True, default=None, null=True)),
                ('ciudadano', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tipo_reporte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shared.tiporeporte')),
            ],
        ),
    ]

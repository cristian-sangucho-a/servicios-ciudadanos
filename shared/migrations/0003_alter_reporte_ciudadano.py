# Generated by Django 5.1 on 2025-01-31 01:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ciudadano_app', '0009_remove_ciudadano_groups_and_more'),
        ('shared', '0002_alter_tiporeporte_departamento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reporte',
            name='ciudadano',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ciudadano_app.ciudadano'),
        ),
    ]

# Generated by Django 5.1 on 2025-01-30 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entidad_municipal_app', '0005_alter_entidadmunicipal_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(help_text='Nombre único del departamento', max_length=150, unique=True, verbose_name='Nombre del Departamento')),
                ('descripcion', models.TextField(blank=True, help_text='Breve descripción del departamento', verbose_name='Descripción')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, help_text='Fecha y hora en que se creó el departamento', verbose_name='Fecha de Creación')),
            ],
        ),
    ]

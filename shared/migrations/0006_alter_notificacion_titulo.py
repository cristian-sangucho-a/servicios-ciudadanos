# Generated by Django 5.1 on 2025-02-03 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shared', '0005_notificacion_titulo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificacion',
            name='titulo',
            field=models.CharField(default='', max_length=255),
        ),
    ]

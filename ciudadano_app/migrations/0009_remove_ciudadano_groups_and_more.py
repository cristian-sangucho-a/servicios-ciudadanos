# Generated by Django 5.1 on 2025-01-31 01:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ciudadano_app', '0008_merge_20250130_1245'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ciudadano',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='ciudadano',
            name='is_superuser',
        ),
        migrations.RemoveField(
            model_name='ciudadano',
            name='user_permissions',
        ),
        migrations.AddField(
            model_name='ciudadano',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='ciudadano',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='ciudadano',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservas', to='ciudadano_app.ciudadano'),
        ),
    ]

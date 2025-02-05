# Generated by Django 5.1 on 2025-02-05 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entidad_municipal_app', '0022_alter_registroasistencia_evento'),
    ]

    operations = [
        migrations.AddField(
            model_name='registroasistencia',
            name='estado_asistencia',
            field=models.CharField(choices=[('PENDIENTE', 'Pendiente'), ('ASISTIO', 'Asistio'), ('NO_ASISTIO', 'No_Asistio')], default='PENDIENTE', help_text='Estado de asistencia del ciudadano al evento', max_length=20, verbose_name='Estado de asistencia'),
        ),
        migrations.AlterField(
            model_name='registroasistencia',
            name='estado_registro',
            field=models.CharField(choices=[('INSCRITO', 'Inscrito'), ('EN_ESPERA', 'En_Espera'), ('CANCELADO', 'Cancelado')], default='INSCRITO', help_text='Estado actual del registro de asistencia', max_length=20, verbose_name='Estado del registro'),
        ),
    ]

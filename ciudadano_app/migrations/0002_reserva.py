# Generated by Django 5.1 on 2025-01-27 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ciudadano_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]

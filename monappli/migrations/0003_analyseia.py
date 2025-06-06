# Generated by Django 5.1.7 on 2025-03-27 14:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monappli', '0002_journalactivite'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnalyseIA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_analyse', models.DateTimeField(auto_now_add=True)),
                ('resultats', models.JSONField()),
                ('succes', models.BooleanField(default=False)),
                ('message', models.TextField(blank=True)),
                ('objet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='analyses', to='monappli.objetdefectueux')),
            ],
            options={
                'verbose_name': 'Analyse IA',
                'verbose_name_plural': 'Analyses IA',
                'ordering': ['-date_analyse'],
            },
        ),
    ]

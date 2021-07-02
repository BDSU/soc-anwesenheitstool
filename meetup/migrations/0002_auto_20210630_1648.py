# Generated by Django 3.2.4 on 2021-06-30 14:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('meetup', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='kategorie',
            field=models.CharField(choices=[('MITGLIEDERSITZUNG', 'Mitgliedersitzung'), ('SCHULUNG', 'Schulung'), ('PROJEKTTREFFEN', 'Projekttreffen'), ('JOUR FIX', 'Jour Fix')], default='MITGLIEDERSITZUNG', max_length=100),
        ),
        migrations.CreateModel(
            name='Anwesenheit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anwesend', models.BooleanField()),
                ('optional', models.BooleanField()),
                ('teilnehmer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
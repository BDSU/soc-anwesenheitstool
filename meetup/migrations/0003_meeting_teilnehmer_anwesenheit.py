# Generated by Django 3.2.4 on 2021-06-30 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetup', '0002_auto_20210630_1648'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='teilnehmer_anwesenheit',
            field=models.ManyToManyField(to='meetup.Anwesenheit'),
        ),
    ]

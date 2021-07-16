# Generated by Django 3.2.5 on 2021-07-16 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetup', '0001_initial'),
    ]

    operations = [
        # unmanaged model
        migrations.CreateModel(
            name='GroupParticipants',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('optional', models.BooleanField()),
            ],
            options={
                'verbose_name': 'Group Participants',
                'verbose_name_plural': 'Group Participants',
                'managed': False,
            },
        ),
        migrations.AlterField(
            model_name='participant',
            name='attendant',
            field=models.BooleanField(default=False),
        ),
    ]
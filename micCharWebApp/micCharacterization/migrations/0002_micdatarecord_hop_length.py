# Generated by Django 4.1.2 on 2022-11-04 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('micCharacterization', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='micdatarecord',
            name='hop_Length',
            field=models.IntegerField(blank=True, default=512),
        ),
    ]

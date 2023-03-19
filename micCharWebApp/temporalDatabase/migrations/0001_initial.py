# Generated by Django 4.1.2 on 2023-03-19 18:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('micCharacterization', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TemporalDatabase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('signal_Graph', models.CharField(default=None, max_length=1000, null=True)),
                ('cepstrum_Graph', models.CharField(default=None, max_length=1000, null=True)),
                ('hilbert_Phase_Graph', models.CharField(default=None, max_length=1000, null=True)),
                ('onset_Strength_Graph', models.CharField(default=None, max_length=1000, null=True)),
                ('lag_Autocorrelation_Graph', models.CharField(default=None, max_length=1000, null=True)),
                ('BPM_Autocorrelation_Graph', models.CharField(default=None, max_length=1000, null=True)),
                ('autocorrelation_Tempogram', models.CharField(default=None, max_length=1000, null=True)),
                ('fourier_Tempogram', models.CharField(default=None, max_length=1000, null=True)),
                ('mic_Data_Record', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='micCharacterization.micdatarecord')),
            ],
        ),
    ]

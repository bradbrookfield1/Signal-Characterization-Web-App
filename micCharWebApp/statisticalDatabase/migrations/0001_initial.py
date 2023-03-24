# Generated by Django 4.1.2 on 2023-03-23 15:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('micCharacterization', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatisticalDatabase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_PDF_Graph', models.CharField(default=None, max_length=1000, null=True)),
                ('harmonic_HPSS_PDF_Graph', models.CharField(default=None, max_length=1000, null=True)),
                ('percussive_HPSS_PDF_Graph', models.CharField(default=None, max_length=1000, null=True)),
                ('welch_PDF_Graph', models.CharField(default=None, max_length=1000, null=True)),
                ('magnitude_FFT_Spectrum_Graph', models.CharField(default=None, max_length=1000, null=True)),
                ('magnitude_FFT_Time_Graph', models.CharField(default=None, max_length=1000, null=True)),
                ('phase_FFT_Spectrum_Graph', models.CharField(default=None, max_length=1000, null=True)),
                ('phase_FFT_Time_Graph', models.CharField(default=None, max_length=1000, null=True)),
                ('magnitude_FMT_Spectrum_Graph', models.CharField(default=None, max_length=1000, null=True)),
                ('magnitude_FMT_Time_Graph', models.CharField(default=None, max_length=1000, null=True)),
                ('phase_FMT_Spectrum_Graph', models.CharField(default=None, max_length=1000, null=True)),
                ('phase_FMT_Time_Graph', models.CharField(default=None, max_length=1000, null=True)),
                ('hilbert_PDF_Graph', models.CharField(default=None, max_length=1000, null=True)),
                ('onset_Strength_PDF_Graph', models.CharField(default=None, max_length=1000, null=True)),
                ('inst_Phase_PDF_Graph', models.CharField(default=None, max_length=1000, null=True)),
                ('signal_Inversion_PDF_Graph', models.CharField(default=None, max_length=1000, null=True)),
                ('mic_Data_Record', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='micCharacterization.micdatarecord')),
            ],
        ),
    ]

# Generated by Django 4.1.2 on 2023-03-22 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statisticalDatabase', '0006_statisticaldatabase_hilbert_pdf_graph'),
    ]

    operations = [
        migrations.AddField(
            model_name='statisticaldatabase',
            name='magnitude_FMT_Spectrum_Graph',
            field=models.CharField(default=None, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='statisticaldatabase',
            name='magnitude_FMT_Time_Graph',
            field=models.CharField(default=None, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='statisticaldatabase',
            name='phase_FMT_Spectrum_Graph',
            field=models.CharField(default=None, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='statisticaldatabase',
            name='phase_FMT_Time_Graph',
            field=models.CharField(default=None, max_length=1000, null=True),
        ),
    ]

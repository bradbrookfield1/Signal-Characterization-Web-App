# Generated by Django 4.1.2 on 2023-03-22 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statisticalDatabase', '0005_statisticaldatabase_magnitude_fft_spectrum_graph_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='statisticaldatabase',
            name='hilbert_PDF_Graph',
            field=models.CharField(default=None, max_length=1000, null=True),
        ),
    ]

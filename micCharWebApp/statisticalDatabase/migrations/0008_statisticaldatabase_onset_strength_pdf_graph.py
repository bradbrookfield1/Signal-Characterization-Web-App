# Generated by Django 4.1.2 on 2023-03-22 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statisticalDatabase', '0007_statisticaldatabase_magnitude_fmt_spectrum_graph_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='statisticaldatabase',
            name='onset_Strength_PDF_Graph',
            field=models.CharField(default=None, max_length=1000, null=True),
        ),
    ]
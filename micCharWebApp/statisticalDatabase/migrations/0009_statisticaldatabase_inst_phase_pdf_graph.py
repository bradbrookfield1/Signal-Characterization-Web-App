# Generated by Django 4.1.2 on 2023-03-22 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statisticalDatabase', '0008_statisticaldatabase_onset_strength_pdf_graph'),
    ]

    operations = [
        migrations.AddField(
            model_name='statisticaldatabase',
            name='inst_Phase_PDF_Graph',
            field=models.CharField(default=None, max_length=1000, null=True),
        ),
    ]
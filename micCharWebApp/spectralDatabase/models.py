from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.urls import reverse
from micCharacterization.models import MicDataRecord

def delete_file_if_unused(model, instance, field, instance_file_field):
    dynamic_field = {}
    dynamic_field[field.name] = instance_file_field.name
    other_refs_exist = model.objects.filter(**dynamic_field).exclude(pk=instance.pk).exists()
    if not other_refs_exist:
        instance_file_field.delete(False)

@receiver(post_delete)
def delete_files_when_row_deleted_from_db(sender, instance, **kwargs):
    for field in sender._meta.concrete_fields:
        if isinstance(field, models.FileField):
            instance_file_field = getattr(instance, field.name)
            delete_file_if_unused(sender, instance, field, instance_file_field)
            
@receiver(pre_save)
def delete_files_when_file_changed(sender, instance, **kwargs):
    if not instance.pk:
        return
    for field in sender._meta.concrete_fields:
        if isinstance(field, models.FileField):
            try:
                instance_in_db = sender.objects.get(pk=instance.pk)
            except sender.DoesNotExist:
                return
            instance_in_db_file_field = getattr(instance_in_db, field.name)
            instance_file_field = getattr(instance, field.name)
            if instance_in_db_file_field.name != instance_file_field.name:
                delete_file_if_unused(sender, instance, field, instance_in_db_file_field)

class SpectralDatabase(models.Model):
    mic_Data_Record = models.OneToOneField(MicDataRecord, on_delete=models.CASCADE)
    average_PSD_Graph = models.CharField(max_length=1000, default=None, null=True)
    noise_PSD_Graph = models.CharField(max_length=1000, default=None, null=True)
    overlapping_PSD_Graph = models.CharField(max_length=1000, default=None, null=True)
    overlapping_Harmonic_PSD_Graph = models.CharField(max_length=1000, default=None, null=True)
    phase_Spectrum_Graph = models.CharField(max_length=1000, default=None, null=True)
    spectrogram = models.CharField(max_length=1000, default=None, null=True)
    mellin_Spectrogram = models.CharField(max_length=1000, default=None, null=True)
    percussive_Spectrogram = models.CharField(max_length=1000, default=None, null=True)
    harmonic_Spectrogram = models.CharField(max_length=1000, default=None, null=True)
    harmonic_Prediction_Graph = models.CharField(max_length=1000, default=None, null=True)
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.pk})
    
    def attributes(self):
        this_dict = self.__dict__
        del this_dict['_state'], this_dict['id'], this_dict['mic_Data_Record_id']
        del this_dict['harmonic_Prediction_Graph']
        for attr, value in this_dict.items():
            yield attr, value
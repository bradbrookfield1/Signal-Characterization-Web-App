import os, copy
from django.db import models
from django.urls import reverse
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

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

class Log(models.Model):
    action = models.CharField(max_length=100)
    record_Name = models.CharField(max_length=100)
    date = models.DateTimeField()
    
    class Meta:
        ordering = ('-date',)

    def get_absolute_url(self):
        return reverse('log-confirm-delete', kwargs={'pk': self.pk})
    
    def get_all_logs():
        return Log.objects.all()

class MicDataRecord(models.Model):
    record_Name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, blank=True)
    prediction_Harmonics = models.IntegerField(blank=True, null=True)
    noisy_Signal_File = models.FileField(upload_to='Recordings/noisy_Signal_File/', blank=True, null=True)
    measured_Signal_File = models.FileField(upload_to='Recordings/measured_Signal_File/', blank=True, null=True)
    noise_File = models.FileField(upload_to='Recordings/noise_File/', blank=True, null=True)
    true_Signal_File = models.FileField(upload_to='Recordings/true_Signal_File/', blank=True, null=True)
    
    class Meta:
        ordering = ('pk',)
    
    def __str__(self):
        return self.record_Name
    
    def get_absolute_url(self):
        return reverse('mic-data-record-detail', kwargs={'pk': self.pk})
    
    def get_all_records():
        return MicDataRecord.objects.all()
    
    def filename(self, attr):
        return eval('os.path.basename(self.' + attr + '.name)')
    
    def get_fileset():
        record_set = MicDataRecord.objects.all().order_by('pk')
        file_set = []
        for record in record_set:
            file_name_list = []
            record_DB_dict = record.__dict__
            record_DB_dict_fixed = copy.deepcopy(record_DB_dict)
            del record_DB_dict_fixed['record_Name'], record_DB_dict_fixed['description'], record_DB_dict_fixed['prediction_Harmonics']
            del record_DB_dict_fixed['_state'], record_DB_dict_fixed['id']
            for attr, value in record_DB_dict_fixed.items():
                if record.filename(attr):
                    file_name_list.append('./Uploads/Recordings/' + attr + '/' + str(record.filename(attr)))
                else:
                    file_name_list.append(None)
            file_set.append(file_name_list)
        return file_set
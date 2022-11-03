import os
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

def delete_file_if_unused(model,instance,field,instance_file_field):
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
        if isinstance(field,models.FileField):
            try:
                instance_in_db = sender.objects.get(pk=instance.pk)
            except sender.DoesNotExist:
                return
            instance_in_db_file_field = getattr(instance_in_db,field.name)
            instance_file_field = getattr(instance,field.name)
            if instance_in_db_file_field.name != instance_file_field.name:
                delete_file_if_unused(sender,instance,field,instance_in_db_file_field)

class Log(models.Model):
    action = models.CharField(max_length=100)
    log_Name = models.CharField(max_length=100)
    date = models.DateTimeField()
    
    class Meta:
        ordering = ('-date',)

    def get_absolute_url(self):
        return reverse('log-confirm-delete', kwargs={'pk': self.pk})

class MicDataRecord(models.Model):
    record_Name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank=True)
    signal_File = models.FileField(upload_to='Uploads/')
    signal_Start = models.IntegerField(blank=True, null=True)
    reference_File = models.FileField(blank=True)
    reference_Start = models.IntegerField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    
    class Meta:
        ordering = ('record_Name',)
    
    def __str__(self):
        return self.record_Name
    
    # def get_all_objects(self):
    #     return MicDataRecord.objects.all()
    
    def get_absolute_url(self):
        return reverse('mic-data-record-detail', kwargs={'pk': self.pk})
    
    def sig_filename(self):
        return os.path.basename(self.signal_File.name)
    
    def ref_filename(self):
        return os.path.basename(self.reference_File.name)
    
    def get_start_dur(self):
        return [self.signal_Start, self.reference_Start, self.duration]
    
    def get_fileset():
        record_set = MicDataRecord.objects.all()
        file_set = []
        for record in record_set:
            file_name = str(record.sig_filename())
            file_set.append(file_name)
        return file_set
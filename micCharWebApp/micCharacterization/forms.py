from django import forms
from .models import MicDataRecord
        
class MicDataRecordForm(forms.ModelForm):

    class Meta:
        model = MicDataRecord
        fields = ['record_Name', 'description', 'signal_File', 'reference_File', 'signal_Start', 'reference_Start', 'duration']
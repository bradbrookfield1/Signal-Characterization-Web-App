from django import forms
from .models import MicDataRecord

class DeleteAllForm(forms.Form):
    class Meta:
        fields = []

class MicDataRecordForm(forms.ModelForm):

    class Meta:
        model = MicDataRecord
        fields = ['record_Name', 'description', 'prediction_Harmonics',
                  'noisy_Signal_File', 'measured_Signal_File', 'noise_File', 'true_Signal_File',
                  'reference_Noisy_Signal_File', 'reference_Signal_File', 'reference_Noise_File']
    
    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('noisy_Signal_File') and not cleaned_data.get('measured_Signal_File') and not cleaned_data.get('noise_File') and not cleaned_data.get('true_Signal_File'):
            raise forms.ValidationError({'noisy_Signal_File': 'At least one from Noisy Signal File, Measured Signal File, Noise File, and True Signal File should be given.'})
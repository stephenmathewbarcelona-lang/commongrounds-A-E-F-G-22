from django import forms
from django.forms import inlineformset_factory

from .models import Commission, Job, JobApplication

class CommissionForm(forms.ModelForm):
    class Meta:
        model = Commission
        fields = ['title', 'description', 'type', 'people_required', 'status']
        widgets = {
            'status': forms.Select(),
        }

JobFormSet = inlineformset_factory(
    Commission,
    Job,
    fields=['role', 'manpower_required', 'status'],
    extra=3,
    can_delete=False,
    widgets={
        'status': forms.Select(),
    }
)

JobFormSetUpdate = inlineformset_factory(
    Commission,
    Job,
    fields=['role', 'manpower_required', 'status'],
    extra=3,
    can_delete=True,
    widgets={
        'status': forms.Select(),
    }
)

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['job', 'applicant', 'status']



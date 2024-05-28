from typing import Any, Mapping
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from assessmentapp.models import AssessmentDetails, AssessmentQuestionnaire

class InitiateAssessmentForm(forms.ModelForm):
    class Meta:
        model = AssessmentDetails
        fields = ['OrgName', 'ProjectName', 'ApplicationName', 'AssessmentFile']

class AssessmentQuestionForm(forms.ModelForm):
    class Meta:
        model = AssessmentQuestionnaire
        fields = ['Domain', 'SubDomain', 'Question', 'Description', 'Remediation', 'Risk', 'Response', 'Remarks']
    
    def __init__(self, *args, **kwargs):
        super(AssessmentQuestionForm, self).__init__(*args, **kwargs)
        self.fields['Domain'].widget.attrs['readonly'] = True
        self.fields['SubDomain'].widget.attrs['readonly'] = True
        self.fields['Question'].widget.attrs['readonly'] = True
        self.fields['Description'].widget.attrs['readonly'] = True
        self.fields['Remediation'].widget.attrs['readonly'] = True
        self.fields['Risk'].widget.attrs['readonly'] = True
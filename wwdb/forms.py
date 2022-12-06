from django import forms
from django.forms import ModelForm
from .models import *


class StartCastForm(ModelForm):
  
    class Meta:
        model = Cast
        widgets = {'startdate': forms.DateInput(attrs={'id': 'datetimepicker12'})}

        fields = [
            "startoperatorid",
            "startdate",
            "deploymenttypeid",
            "winchid",
            "notes",
        ]

class EndCastForm(ModelForm):
  
    class Meta:
        model = Cast
  
        fields = [
            "endoperatorid",
            "enddate",
            "notes",
        ]

class EditCastForm(ModelForm):
  
    class Meta:
        model = Cast
  
        fields = [
            'startoperatorid',
            'endoperatorid',
            'startdate',
            'deploymenttypeid',
            'winchid',
            'notes'
        ]
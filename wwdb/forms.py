from django import forms
from django.forms import ModelForm
from .models import *
from bootstrap_datepicker_plus.widgets import DateTimePickerInput

class StartCastForm(ModelForm):
  
    class Meta:
        model = Cast

        fields = [
            'startoperatorid',
            'startdate',
            'deploymenttypeid',
            'winchid',
            'notes',
        ]

        widgets = {'startdate': DateTimePickerInput()}


class EndCastForm(ModelForm):
  
    class Meta:
        model = Cast
  
        fields = [
            'endoperatorid',
            'enddate',
            'notes',
        ]

        widgets = {'enddate': DateTimePickerInput()}

class EditCastForm(ModelForm):
  
    class Meta:
        model = Cast
  
        fields = [
            'startoperatorid',
            'endoperatorid',
            'startdate',
            'enddate',
            'deploymenttypeid',
            'winchid',
            'notes'
        ]

        widgets = {'startdate': DateTimePickerInput(), 
                   'enddate': DateTimePickerInput()}
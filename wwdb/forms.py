from django import forms
from django.forms import ModelForm
from .models import *

class StatusForm(forms.ModelForm):
    class Meta:
        model = WinchOperator
        fields = ['status', ]

        widgets = {
            'status': forms.CheckboxInput(
                    attrs={"class": "form-check-input", "id": "flexSwitchCheckChecked"})
        }

"""
class DateInput(forms.DateInput):
    input_type = 'time'


# creating a form
class startcastform(ModelForm):
  
    # create meta class
    class Meta:
        # specify model to be used
        model = Cast
  
        # specify fields to be used
        fields = [
            "operatorid",
            "startdate",
            "deploymenttypeid",
            "winchid",
            "notes",

        ]

# creating a form
class endcastform(ModelForm):
  
    # create meta class
    class Meta:
        # specify model to be used
        model = Cast
  
        # specify fields to be used
        fields = [
            "operatorid",
            "enddate",
            "notes",

        ]
"""
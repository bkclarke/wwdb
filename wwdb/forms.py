from django import forms
from django.forms import ModelForm
from .models import *

"""
class StartCastForm(ModelForm):
  
    class Meta:
        model = Cast
  
        fields = [
            "startoperatorid",
            "startdate",
            "deploymenttypeid",
            "winchid",
            "notes",
        ]

class FolderForm(forms.ModelForm):
    class Meta:
       model = Folder
       fields = ['name', 'parent']

    def __init__(self, *args, **kwargs):
       user = kwargs.pop('user')
       super(FolderForm, self).__init__(*args, **kwargs)
       self.fields['parent'].queryset = Folder.objects.filter(user=user)

class StatusForm(forms.ModelForm):
    class Meta:
        model = WinchOperator
        fields = ['status', ]

        widgets = {
            'status': forms.CheckboxInput(
                    attrs={"class": "form-check-input", "id": "flexSwitchCheckChecked"})
        }

class DateInput(forms.DateInput):
    input_type = 'time'


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
from django import forms
from django.forms import ModelForm
from .models import *
from bootstrap_datepicker_plus.widgets import DateTimePickerInput

class StartCastForm(ModelForm):
    flagforreview = forms.BooleanField()

    class Meta:
        model = Cast
        fields = [
            'startoperatorid',
            'startdate',
            'deploymenttypeid',
            'winchid',
            'notes',
            'flagforreview',
        ]

        widgets = {'startdate': DateTimePickerInput()}

class EndCastForm(ModelForm):
    flagforreview = forms.BooleanField()
  
    class Meta:
        model = Cast
  
        fields = [
            'endoperatorid',
            'enddate',
            'notes',
            'flagforreview',
        ]

        widgets = {'enddate': DateTimePickerInput()}

class EditCastForm(ModelForm):
    flagforreview = forms.BooleanField()
  
    class Meta:
        model = Cast
  
        fields = [
            'startoperatorid',
            'endoperatorid',
            'startdate',
            'enddate',
            'deploymenttypeid',
            'winchid',
            'notes',
            'flagforreview',
        ]

        widgets = {'startdate': DateTimePickerInput(), 
                   'enddate': DateTimePickerInput()}

class EditFactorofSafetyForm(ModelForm):
  
    class Meta:
        model = Wire
  
        fields = [
            'factorofsafety',
        ]

class EditWinchStatusForm(ModelForm):
  
    class Meta:
        model = Winch
  
        fields = [
            'status',
        ]
        
class EditOperatorStatusForm(ModelForm):
  
    class Meta:
        model = WinchOperator
  
        fields = [
            'status',
        ]

class EditDeploymentStatusForm(ModelForm):
  
    class Meta:
        model = DeploymentType
  
        fields = [
            'status',
        ]
from django import forms
from django.forms import ModelForm
from .models import *
from bootstrap_datepicker_plus.widgets import DatePickerInput, DateTimePickerInput
from django.forms.widgets import HiddenInput
from datetime import datetime


class StartCastForm(ModelForm):
    flagforreview = forms.BooleanField(required=False)

    class Meta:
        model = Cast
        fields = [
            'cruisenumber',
            'startoperator',
            'startdate',
            'deploymenttype',
            'winch',
            'notes',
            'flagforreview',
        ]

        widgets = {'startdate': DateTimePickerInput()}

class EndCastForm(ModelForm):
    flagforreview = forms.BooleanField(required=False)
  
    class Meta:
        model = Cast
  
        fields = [
            'endoperator',
            'startdate',
            'enddate',
            'notes',
            'flagforreview',
        ]

        widgets = {'startdate': DateTimePickerInput(), 
                    'enddate': DateTimePickerInput(),
                    'startdate': forms.HiddenInput(),}

        
    def is_valid(self):
        valid = super().is_valid()

        if hasattr(self, 'cleaned_data') and valid:

            start_date = self.cleaned_data.get('startdate')
            end_date = self.cleaned_data.get('enddate')
            if not end_date:
                self.add_error('enddate', 'Please enter end date')
                valid = False
            elif end_date < start_date:
                self.add_error('enddate', 'End date must be greater than start date')
                valid = False
        return valid     


class EditCastForm(ModelForm):
    flagforreview = forms.BooleanField(required=False)
  
    class Meta:
        model = Cast
  
        fields = [
            'startoperator',
            'endoperator',
            'startdate',
            'enddate',
            'deploymenttype',
            'winch',
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

class AddDeploymentForm(ModelForm):

    class Meta:
        model = DeploymentType
        fields = [
            'name',
            'equipment',
            'notes',
            'status',
        ]

class EditCruiseForm(ModelForm):
  
    class Meta:
        model = Cruise
  
        fields = [
            'number',
            'startdate',
            'status',
        ]
 
        widgets = {'startdate': DatePickerInput(
                    options={
                    "format": "YYYY-MM-DD"}
                    )}

class AddCutbackReterminationForm(ModelForm):

    class Meta:
        model = CutbackRetermination
        fields = [
            'date',
            'wire',
            'wetendtag',
            'lengthremoved',
            'notes',
        ]

        widgets = {'date': DatePickerInput(
                    options={
                    "format": "YYYY-MM-DD"}
                    )}

class EditCutbackReterminationForm(ModelForm):
  
    class Meta:
        model = CutbackRetermination
  
        fields = [
            'date',
            'wire',
            'wetendtag',
            'lengthremoved',
            'notes',
        ]

        widgets = {'date': DatePickerInput(
                    options={
                    "format": "YYYY-MM-DD"}
                    )}


class EditWireDrumForm(ModelForm):
  
    class Meta:
        model = Wiredrum
  
        fields = [
            'date',
            'drum',
            'wire',
            'notes',
        ]

        widgets = {'date': DatePickerInput(
                options={
                "format": "YYYY-MM-DD"}
                )}

class WireDrumAddForm(ModelForm):

    class Meta:
        model = Wiredrum
        fields = [
            'wire',
            'drum',
            'date',
            'notes',
        ]

        widgets = {'date': DatePickerInput(
                    options={
                    "format": "YYYY-MM-DD"}
                    )}

class AddDrumForm(ModelForm):

    class Meta:
        model = Drum
        fields = [
            'internalid',
            'color',
            'size',
            'weight',
            'location',
            'material',
            'wiretype',
        ]

class EditDrumForm(ModelForm):
  
    class Meta:
        model = Drum
  
        fields = [
            'internalid',
            'color',
            'size',
            'weight',
            'location',
            'material',
            'wiretype',
        ]

class CruiseAddForm(ModelForm):

    class Meta:
        model = Cruise
        fields = [
            'number',
            'startdate',
            'status',
        ]

        widgets = {'startdate': DatePickerInput(
                    options={
                    "format": "YYYY-MM-DD"}
                    )}

class AddOperatorForm(ModelForm):

    class Meta:
        model = WinchOperator
        fields = [
            'firstname',
            'lastname',
            'username',
            'status',
        ]

class DrumLocationAddForm(ModelForm):

    class Meta:
        model = DrumLocation
        fields = [
            'date',
            'enteredby',
            'drumid',
            'winch',
            'location',
            'notes',
        ]

        widgets = {'date': DatePickerInput(
                    options={
                    "format": "YYYY-MM-DD"}
                    )}

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
            'startoperator',
            'startdate',
            'deploymenttype',
            'winch',
			'motor',
            'notes',
            'flagforreview',
        ]

        widgets = {'startdate': DateTimePickerInput()}


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        active_operators = WinchOperator.objects.filter(status=True)
        active_winches = Winch.objects.filter(status=True)
        active_deployments = DeploymentType.objects.filter(status=True)
        self.fields['startoperator'].queryset  = active_operators
        self.fields['winch'].queryset  = active_winches
        self.fields['deploymenttype'].queryset  = active_deployments


class ManualCastForm(ModelForm):

    class Meta:
        model = Cast
        fields = [
            'startoperator',
            'endoperator',
            'startdate',
            'enddate',
            'deploymenttype',
            'winch',
			'motor',
            'notes',
            'maxtension',
            'maxpayout',
        ]

        widgets = {'startdate': DateTimePickerInput(), 
                   'enddate': DateTimePickerInput()}

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        active_operators = WinchOperator.objects.filter(status=True)
        self.fields['endoperator'].queryset  = active_operators

        
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
            'firstname',
            'lastname',
            'username',
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
            'enddate',
            'winch1status',
            'winch2status',
            'winch3status',
            'winch1blockarrangement',
            'winch2blockarrangement',
            'winch3blockarrangement',
            'winch3blockarrangement',
            'winch1termination',
            'winch2termination',
            'winch3termination',
            'winch1notes',
            'winch2notes',
            'winch3notes',
            'winch2spindirection',
            'scienceprovidedwinch',
        ]
 
        widgets = {'startdate': DatePickerInput(
                    options={
                    "format": "YYYY-MM-DD"}
                    ),
                   'enddate': DatePickerInput(
                    options={
                    "format": "YYYY-MM-DD"}
                    )}


class EditCruiseMetaForm(ModelForm):
  
    class Meta:
        model = Cruise
  
        fields = [
            'winch1status',
            'winch2status',
            'winch3status',
            'winch1blockarrangement',
            'winch2blockarrangement',
            'winch3blockarrangement',
            'winch3blockarrangement',
            'winch1termination',
            'winch2termination',
            'winch3termination',
            'winch2spindirection',
            'scienceprovidedwinch',
        ]

class EditCruiseReportForm(ModelForm):
  
    class Meta:
        model = Cruise
  
        fields = [
            'startdate',
            'enddate',
            'winch1blockarrangement',
            'winch2blockarrangement',
            'winch3blockarrangement',
            'winch1termination',
            'winch2termination',
            'winch3termination',
            'winch2spindirection',
            'winch1notes',
            'winch2notes',
            'winch3notes',
            'scienceprovidedwinch',
        ]
 
        widgets = {'startdate': DatePickerInput(
                    options={
                    "format": "YYYY-MM-DD"}
                    ),
                   'enddate': DatePickerInput(
                    options={
                    "format": "YYYY-MM-DD"}
                    )}

'''
class EditCruiseWinchForm(ModelForm):
  
    class Meta:
        model = Cruise
  
        fields = [
            'winch1',
            'winch2',
            'winch3',
        ]
'''

class AddCutbackReterminationForm(ModelForm):

    class Meta:
        model = CutbackRetermination
        fields = [
            'date',
            'wire',
            'wetendtag',
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


class AddDrumLocationForm(ModelForm):

    class Meta:
        model = DrumLocation
        fields = [
            'date',
            'enteredby',
            'drumid',
            'location',
            'notes',
            'winch',
        ]

class EditDrumLocationForm(ModelForm):
  
    class Meta:
        model = DrumLocation
  
        fields = [
            'date',
            'enteredby',
            'drumid',
            'location',
            'notes',
            'winch',
        ]

class CruiseAddForm(ModelForm):
    winch1status = forms.BooleanField(required=False)
    winch2status = forms.BooleanField(required=False)
    winch3status = forms.BooleanField(required=False)

    class Meta:
        model = Cruise
        fields = [
            'number',
            'startdate',
            'enddate',
            'winch1status',
            'winch2status',
            'winch3status',
        ]

        widgets = {'startdate': DatePickerInput(
                    options={
                    "format": "YYYY-MM-DD"}
                    ),
					'enddate': DatePickerInput(
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

class CruiseReportForm(forms.Form):
    start_date = forms.DateField()
    end_date = forms.DateField()

    widgets = {'start_date': DateTimePickerInput(), 
            'end_date': DateTimePickerInput(),}
    
    def clean_start_date(self):
        start = self.cleaned_data['start_date']
        end = self.cleaned_data['end_date']

        if end < start:
            raise ValidationError(_('end date must be after start date'))

        return data
		
class WinchAddForm(ModelForm):

    class Meta:
        model = Winch
        fields = [
            'name',
            'institution',
            'status',
        ]

class UnolsWireReportForm(ModelForm):

    class Meta:
        model = Cast
        fields = [
            'startdate',
            'enddate',
        ]

        widgets = {'startdate': DateTimePickerInput(), 
                   'enddate': DateTimePickerInput()}

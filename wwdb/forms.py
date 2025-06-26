from django import forms
from django.forms import ModelForm
from .models import *
from bootstrap_datepicker_plus.widgets import DatePickerInput, DateTimePickerInput
from django.forms.widgets import HiddenInput, Widget
from datetime import datetime
from django.core.exceptions import ValidationError
from django.forms import modelformset_factory



class StartCastForm(ModelForm):
    flagforreview = forms.BooleanField(required=False)
    deploymenttype = forms.ModelChoiceField(DeploymentType.objects.filter(status=True), widget=forms.Select(attrs={'class': 'form-control'}))
    winch = forms.ModelChoiceField(Winch.objects.filter(status=True), widget=forms.Select(attrs={'class': 'form-control'}))
    motor = forms.ModelChoiceField(Motor.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    startoperator = forms.ModelChoiceField(WinchOperator.objects.filter(status=True), widget=forms.Select(attrs={'class': 'form-control'}))


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

        widgets = {
            'startdate': DateTimePickerInput(),
            "notes": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 100%; align: center;",
                    "placeholder": "Notes",
                }),
            }

class StartEndCastForm(ModelForm):
    flagforreview = forms.BooleanField(required=False)
    wirerinse = forms.BooleanField(required=False)
    deploymenttype = forms.ModelChoiceField(DeploymentType.objects.filter(status=True), widget=forms.Select(attrs={'class': 'form-control'}))
    winch = forms.ModelChoiceField(Winch.objects.filter(status=True), widget=forms.Select(attrs={'class': 'form-control'}))
    startoperator = forms.ModelChoiceField(WinchOperator.objects.filter(status=True), widget=forms.Select(attrs={'class': 'form-control'}))
    endoperator = forms.ModelChoiceField(WinchOperator.objects.filter(status=True), widget=forms.Select(attrs={'class': 'form-control'}))

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
            'flagforreview',
        ]

        widgets = {
            "notes": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 100%; align: center;",
                    "placeholder": "Notes",
                }
            ),
            'startdate': DateTimePickerInput(), 
            'enddate': DateTimePickerInput()
            }

"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        active_operators = WinchOperator.objects.filter(status=True)
        active_winches = Winch.objects.filter(status=True)
        active_deployments = DeploymentType.objects.filter(status=True)
        self.fields['startoperator'].queryset  = active_operators
        self.fields['winch'].queryset  = active_winches
        self.fields['deploymenttype'].queryset  = active_deployments
"""

class ManualCastForm(ModelForm):
    wirerinse = forms.BooleanField(required=False)

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
            'wirerinse',
        ]

        widgets = {'startdate': DateTimePickerInput(), 
                   'enddate': DateTimePickerInput()}

class EndCastForm(ModelForm):
    flagforreview = forms.BooleanField(required=False)
    wirerinse = forms.BooleanField(required=False)
    endoperator = forms.ModelChoiceField(WinchOperator.objects.filter(status=True), widget=forms.Select(attrs={'class': 'form-control'}))

  
    class Meta:
        model = Cast
  
        fields = [
            'endoperator',
            'enddate',
            'notes',
            'wirerinse',
            'flagforreview',
        ]

        widgets = {
            'enddate': DateTimePickerInput(),
            "notes": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 100%; align: center;",
                    "placeholder": "Notes",
                }),
            }

"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        active_operators = WinchOperator.objects.filter(status=True)
        self.fields['endoperator'].queryset  = active_operators
"""

"""       
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
"""

class EditCastForm(ModelForm):
    flagforreview = forms.BooleanField(required=False)
    wirerinse = forms.BooleanField(required=False)
  
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
            'wirerinse',
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
    
class WinchOperatorTableForm(forms.ModelForm):
    status = forms.BooleanField(required=False)

    class Meta:
        model = WinchOperator
        exclude = []

        widgets = {
            "firstname": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 450px; align: center;",
                    "placeholder": "Title",
                }
            ),
            "lastname": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 450px; align: center;",
                    "placeholder": "Title",
                }
            ),
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 450px; align: center;",
                    "placeholder": "Title",
                }
            ),
        }

class CruiseTableForm(forms.ModelForm):
    class Meta:
        model = Cruise
        exclude = []

        widgets = {
            'startdate': DatePickerInput(), 
            'enddate': DatePickerInput(),
            "number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 450px; align: center;",
                    "placeholder": "cruise number",
                }),
            "winch1termination": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 450px; align: center;",
                    "placeholder": "cruise number",
                }),
            "winch1blockarrangement": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 450px; align: center;",
                    "placeholder": "cruise number",
                }),
            "winch1notes": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 450px; align: center;",
                    "placeholder": "cruise number",
                }),
            "winch2termination": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 450px; align: center;",
                    "placeholder": "cruise number",
                }),
            "winch2blockarrangement": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 450px; align: center;",
                    "placeholder": "cruise number",
                }),
            "winch2notes": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 450px; align: center;",
                    "placeholder": "cruise number",
                }),
            "winch3termination": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 450px; align: center;",
                    "placeholder": "cruise number",
                }),
            "winch3blockarrangement": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 450px; align: center;",
                    "placeholder": "cruise number",
                }),
            "winch3notes": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 450px; align: center;",
                    "placeholder": "cruise number",
                }),
            "scienceprovidedwinch": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 450px; align: center;",
                    "placeholder": "cruise number",
                }),
        }

class DeploymentTableForm(forms.ModelForm):
    status = forms.BooleanField(required=False)

    class Meta:
        model = DeploymentType
        exclude = []

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 450px; align: center;",
                    "placeholder": "name",
                }),
            "equipment": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 450px; align: center;",
                    "placeholder": "equipment details",
                }),
            "notes": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 450px; align: center;",
                    "placeholder": "notes",
                }),
        }

class WinchTableForm(forms.ModelForm):
    status = forms.BooleanField(required=False)

    class Meta:
        model = Winch
        exclude = []

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 450px; align: center;",
                    "placeholder": "name",
                }),
        }


class SWTTableForm(forms.ModelForm):
    class Meta:
        model = Wire
        exclude = []

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
                    ),
                "number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 450px; align: center;",
                    "placeholder": "number",
                }),
                "winch1blockarrangement": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 450px; align: center;",
                    "placeholder": "winch1blockarrangement",
                }),
                "winch2blockarrangement": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 450px; align: center;",
                    "placeholder": "winch2blockarrangement",
                }),
                "winch3blockarrangement": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 450px; align: center;",
                    "placeholder": "winch3blockarrangement",
                }),
                "winch1termination": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 450px; align: center;",
                    "placeholder": "winch1termination",
                }),
                "winch2termination": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 450px; align: center;",
                    "placeholder": "winch2termination",
                }),
                "winch3termination": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 450px; align: center;",
                    "placeholder": "winch3termination",
                }),
                "winch1notes": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 450px; align: center;",
                    "placeholder": "winch1notes",
                }),
                "winch2notes": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 450px; align: center;",
                    "placeholder": "winch2notes",
                }),
                "winch3notes": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 450px; align: center;",
                    "placeholder": "winch3notes",
                }),
                "winch2spindirection": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 450px; align: center;",
                    "placeholder": "winch2spindirection",
                }),
                "scienceprovidedwinch": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 450px; align: center;",
                    "placeholder": "scienceprovidedwinch",
                }),
                }


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


        widgets = {
            "notes": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 100%; align: center;",
                    "placeholder": "Notes",
                }
            ),
            'date': DatePickerInput(
                    options={
                    "format": "YYYY-MM-DD"}
        )}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['wetendtag'].required = True
        self.fields['date'].required = True

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
                    ),
                    "notes": forms.TextInput(
                    attrs={
                        "class": "form-control",
                        "style": "max-width: 100%; align: center;",
                        "placeholder": "notes",
                }),
                }


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


class LubricationAddForm(ModelForm):

    class Meta:
        model = Lubrication
        fields = [
            'wire',
            'lubetype',
            'date',
            'lubelength',
            'lubestartmetermark',
            'lubeendmetermark',
            'notes',
        ]

        widgets = {'date': DatePickerInput(), 
                "lubetype": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 100%; align: center;",
                    "placeholder": "lubetype",
                }),
                "notes": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 100%; align: center;",
                    "placeholder": "notes",
                }),
                   }

class BreaktestEditForm(ModelForm):

    class Meta:
        model = Breaktest
        fields = [
            'date',
            'wire',
            'testedbreakingload',
            'notes',
        ]

        widgets = {
                'date': DatePickerInput(
                    options={
                    "format": "YYYY-MM-DD"}),
                "notes": forms.TextInput(
                    attrs={
                        "class": "form-control",
                        "style": "max-width: 100%; align: center;",
                        "placeholder": "notes",
                }),
            }

class BreaktestAddForm(ModelForm):
  
    class Meta:
        model = Breaktest
  
        fields = [
            'date',
            'wire',
            'testedbreakingload',
            'notes',
        ]

        widgets = {'date': DatePickerInput(
                    options={
                    "format": "YYYY-MM-DD"}
                    ),
                    "notes": forms.TextInput(
                    attrs={
                        "class": "form-control",
                        "style": "max-width: 100%; align: center;",
                        "placeholder": "notes",
                }),
                }

class CastFilterForm(forms.Form):
    winch = forms.ModelChoiceField(queryset=Winch.objects.all(), empty_label='All winches', required=False)
    deploymenttype = forms.ModelChoiceField(queryset=DeploymentType.objects.all(), empty_label='All deployments', required=False)
    operator = forms.ModelChoiceField(queryset=WinchOperator.objects.all(), empty_label='All operators', required=False)
    wire = forms.ModelChoiceField(queryset=Wire.objects.all(), empty_label='All wires', required=False)
    startdate = forms.DateTimeField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    enddate = forms.DateTimeField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))


class DataFilterForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    winch = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['winch'].choices = [(winch.id, winch.name) for winch in Winch.objects.all()]

class WireRopeDataEditForm(ModelForm):

    class Meta:
        model = WireRopeData
        fields = [
            'name',
            'manufacturer',
            'manufacturerpartnumber',
            'cabletype',
            'nominalbreakingload',
            'weightperfoot',

        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: ;100% align: center;",
                    "placeholder": "name",
                }),
            "manufacturer": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: ;100% align: center;",
                    "placeholder": "name",
                }),
            "manufacturerpartnumber": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 100%; align: center;",
                    "placeholder": "name",
                }),
            "cabletype": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 100%; align: center;",
                    "placeholder": "name",
                }),
        }

class WireRopeDataAddForm(ModelForm):

    class Meta:
        model = WireRopeData
        fields = [
            'name',
            'manufacturer',
            'manufacturerpartnumber',
            'cabletype',
            'nominalbreakingload',
            'weightperfoot',

        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: ;100% align: center;",
                    "placeholder": "name",
                }),
            "manufacturer": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: ;100% align: center;",
                    "placeholder": "manufacturer",
                }),
            "manufacturerpartnumber": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 100%; align: center;",
                    "placeholder": "manufacturer part number",
                }),
            "cabletype": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 100%; align: center;",
                    "placeholder": "cable type",
                }),
        }


class CalibrationWorksheetForm(ModelForm):
    class Meta:
        model = Calibration
        fields = ['date', 'operator', 'winch', 'weightofgear', 'notes']
        widgets = {
            'date': DatePickerInput(
                options={"format": "YYYY-MM-DD"}
            ),
            'notes': forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 100%;",
                    "placeholder": "notes",
                }
            ),
            'operator': forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 100%;",
                    "placeholder": "name",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set required fields
        self.fields['date'].required = True
        self.fields['operator'].required = True
        self.fields['winch'].required = True

class TensionVerificationForm(forms.ModelForm):
    class Meta:
        model = TensionVerification
        fields = ['appliedload', 'loadcelltension', 'loadcellrawmv']
        widgets = {
            'appliedload': forms.NumberInput(attrs={'class': 'appliedload form-control'}),
            'loadcelltension': forms.NumberInput(attrs={'class': 'loadcelltension form-control'}),
            'loadcellrawmv': forms.NumberInput(attrs={'class': 'loadcellrawmv form-control'}),
        }

class TensionCalibrationForm(forms.ModelForm):
    class Meta:
        model = TensionCalibration
        fields = ['appliedload', 'loadcelltension', 'loadcellrawmv']
        widgets = {
            'appliedload': forms.NumberInput(attrs={'class': 'appliedload form-control'}),
            'loadcelltension': forms.NumberInput(attrs={'class': 'loadcelltension form-control'}),
            'loadcellrawmv': forms.NumberInput(attrs={'class': 'loadcellrawmv form-control'}),
        }

class CalibrationVerificationForm(forms.ModelForm):
    class Meta:
        model = CalibrationVerification
        fields = ['appliedload', 'loadcelltension', 'loadcellrawmv']
        widgets = {
            'appliedload': forms.NumberInput(attrs={'class': 'appliedload form-control'}),
            'loadcelltension': forms.NumberInput(attrs={'class': 'loadcelltension form-control'}),
            'loadcellrawmv': forms.NumberInput(attrs={'class': 'loadcellrawmv form-control'}),
        }

TensionVerificationFormSet = modelformset_factory(
    TensionVerification,
    form=TensionVerificationForm,
    extra=2,
    can_delete=False
)

TensionCalibrationFormSet = modelformset_factory(
    TensionCalibration,
    form=TensionCalibrationForm,
    extra=2,
    can_delete=False
)

CalibrationVerificationFormSet = modelformset_factory(
    CalibrationVerification,
    form=CalibrationVerificationForm,
    extra=3,
    can_delete=False
)
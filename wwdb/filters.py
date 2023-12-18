import django_filters
from django_filters import DateFilter
from bootstrap_datepicker_plus.widgets import DatePickerInput, DateTimePickerInput
from django import forms

from .models import *

class DateInput(forms.DateInput):
    input_type='date'

class CastFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='startdate', lookup_expr='gte', widget = DateInput(attrs={'type': 'date'}))
    end_date = DateFilter(field_name='enddate', lookup_expr='lte', widget = DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Cast
        fields =['deploymenttype','winch']

            
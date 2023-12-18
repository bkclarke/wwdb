from django import template
from django.db.models.query import QuerySet
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader

from wwdb.filters import CastFilter
from .models import *
from django.views.generic import *
from django.urls import reverse_lazy
from django.urls import reverse
from bootstrap_datepicker_plus import *
from .forms import *
from django.shortcuts import render, get_object_or_404, redirect
import pandas as pd
from django.db.models import Count, Q
import pyodbc 
from django.db.models import Avg, Count, Min, Sum, Max
import logging
from .filters import *
import json

logger = logging.getLogger(__name__)

def home(request):
    template = loader.get_template('wwdb/home.html')
    context = {}
    return HttpResponse(template.render(context, request))

"""
CASTS
Classes related to create, update, delete, view Cast model
"""

def caststart(request):
    context ={}
    form = StartCastForm(request.POST or None)
    if request.method == "POST":
        form = StartCastForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            castid=Cast.objects.last()
            return HttpResponseRedirect("%i/castend" % castid.pk)
    else:
        form = StartCastForm 
        if 'submitted' in request.GET:
            submitted = True
            return render(request, 'wwdb/casts/caststart.html', {'form':form, 'submitted':submitted, 'id':id})

    context['form']= form

    return render(request, "wwdb/casts/caststart.html", context)

def castlist(request):
    cast_uricomplete = Cast.objects.filter(flagforreview=False, maxpayout__isnull=False, payoutmaxtension__isnull=False, maxtension__isnull=False) 
    cast_flag = Cast.objects.filter((Q(winch=1) | Q(winch=2) | Q(winch=3)), (Q(flagforreview=True) | Q(maxpayout__isnull=True) | Q(payoutmaxtension__isnull=True) | Q(maxtension__isnull=True)))
    
    myfilter = CastFilter(request.GET, queryset=cast_uricomplete)
    cast_noflag = myfilter.qs

    context = {
        'cast_uricomplete': cast_uricomplete,
        'cast_flag': cast_flag,
        'myfilter':myfilter,
       }

    return render(request, 'wwdb/reports/castlist.html', context=context)

def cast_end(request):
    last = Cast.objects.latest('pk')
    return redirect('castend', id=last.pk)
	
def castend(request, id):
    context ={}
    obj = get_object_or_404(Cast, id = id)
    form = EndCastForm(request.POST or None, instance = obj)
    if request.method == 'POST':
        cast=Cast.objects.last()
        if form.is_valid():
            form.save()
            cast.refresh_from_db()
            cast.endcastcal()
            cast.save()
            return HttpResponseRedirect("/wwdb/casts/%i/castenddetail" % cast.pk)
    context["form"] = form
    return render(request, "wwdb/casts/castend.html", context)

def castedit(request, id):
    context ={}
    obj = Cast.objects.get(id=id)
    if request.method == 'POST':
        form = EditCastForm(request.POST, instance = obj)
        if form.is_valid():
            form.save()
            obj.endcastcal()
            obj.save()
            return HttpResponseRedirect('/wwdb/reports/castlist')
    else:
        form = EditCastForm(instance = obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/wwdb/casts/%i/edit' % cast.pk)

    context["form"] = form
    return render(request, "wwdb/casts/castedit.html", context)

def castdetail(request, id):
    context ={}
    context["cast"] = Cast.objects.get(id = id)     
    return render(request, "wwdb/casts/castdetail.html", context)

class CastDelete(DeleteView):
    model = Cast
    template_name="wwdb/casts/castdelete.html"
    success_url= reverse_lazy('castlist')

def castenddetail(request, id):
    context ={}
    context["cast"] = Cast.objects.get(id = id)
    return render(request, "wwdb/casts/castenddetail.html", context)

"""
PRECRUISE CONFIGURATION
Classes related to starting a cruise including updating WinchOperators and DeploymentType models
"""

def cruiseconfigurehome(request):
    operators = WinchOperator.objects.all()
    deployments = DeploymentType.objects.all()
    active_wire = Wire.objects.filter(status=True)
    winches = Winch.objects.all()
    cruise = Cruise.objects.all()

    context = {
        'operators': operators,
        'deployments': deployments,
        'active_wire': active_wire,
        'winches': winches,
        'cruise' : cruise,
       }

    return render(request, 'wwdb/configuration/cruiseconfiguration.html', context=context)

def wireeditfactorofsafety(request, id):
    context ={}
    obj = get_object_or_404(Wire, id = id)

    if request.method == 'POST':
        form = EditFactorofSafetyForm(request.POST, instance = obj)
        if form.is_valid():
            form.save()
            wireid=Wire.objects.get(id=id)
            return HttpResponseRedirect("/wwdb/configuration/cruiseconfiguration")
    else:
        form = EditFactorofSafetyForm(instance = obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/wwdb/inventories/wire/%i/editfactorofsafety" % wireid.pk)

    context["form"] = form
    return render(request, "wwdb/inventories/wireeditfactorofsafety.html", context)


"""
WINCH WIRE REPORTING
Classes related to winch and wire reporting 
"""

def wirereport(request, pk):
    wire=Wire.objects.filter(id=pk)
    wire_object=wire.last()
    wire_drum=Wiredrum.objects.filter(wire=pk)
    cutback_retermination=CutbackRetermination.objects.filter(wire=pk)
    break_test=Breaktest.objects.filter(wire=pk)

    context ={
        'wire':wire,
        'wire_object':wire_object,
        'wire_drum':wire_drum,
        'cutback_retermination':cutback_retermination,
        'break_test':break_test,
        }

    return render(request, "wwdb/reports/wirereport.html", context)

def cruiselist(request):
    cruises = Cruise.objects.order_by('-startdate')

    context = {
        'cruises': cruises,
       }

    return render(request, 'wwdb/reports/cruiselist.html', context=context)


def cruisereportedit(request, pk):
    obj = get_object_or_404(Cruise, id = pk)

    #cruise object and casts by cruise daterange
    cruise_object=obj
    startdate=cruise_object.startdate
    enddate=cruise_object.enddate
    casts=Cast.objects.filter(startdate__range=[startdate, enddate])

    #winch status objects
    winch1=cruise_object.winch1
    winch2=cruise_object.winch2
    winch3=cruise_object.winch3

    #winch 1 casts calculations
    casts_winch1=casts.filter(winch='3')
    casts_winch1_count=casts_winch1.count()

    #winch 2 casts calculations
    casts_winch2=casts.filter(winch='2')
    casts_winch2_count=casts_winch2.count()

    #winch 3 casts calculations
    casts_winch3=casts.filter(winch='1')
    casts_winch3_count=casts_winch3.count()

    if request.method == 'POST':
        form = EditCruiseReportForm(request.POST, instance = obj)
        if form.is_valid():
            form.save()
            cruiseid=Cruise.objects.get(id=pk)
            return HttpResponseRedirect("/wwdb/reports/%i/cruisereport" % cruiseid.pk)
    else:
        form = EditCruiseReportForm(instance = obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/wwdb/reports/%i/cruisereportedit" % cruiseid.pk)
    
    context ={
        'casts_winch1_count':casts_winch1_count,
        'casts_winch2_count':casts_winch2_count,
        'casts_winch3_count':casts_winch3_count,
        }

    context["form"] = form
    return render(request, "wwdb/reports/cruisereportedit.html", context)

def cruisereport(request, pk):
    

    #cruise object and casts by cruise daterange
    cruise=Cruise.objects.filter(id=pk)
    cruise_object=cruise.last()
    startdate=cruise_object.startdate
    enddate=cruise_object.enddate
    casts=Cast.objects.filter(startdate__range=[startdate, enddate])

    #winch status objects
    winch1=cruise_object.winch1
    winch2=cruise_object.winch2
    winch3=cruise_object.winch3

    #winch 1 casts calculations
    casts_winch1=casts.filter(winch='3')
    casts_winch1_count=casts_winch1.count()
    casts_winch1_maxtension=casts_winch1.order_by('maxtension').last()
    casts_winch1_maxpayout=casts_winch1.order_by('maxpayout').last()

    #winch 2 casts calculations
    casts_winch2=casts.filter(winch='2')
    casts_winch2_count=casts_winch2.count()
    casts_winch2_maxtension=casts_winch2.order_by('maxtension').last()
    casts_winch2_maxpayout=casts_winch2.order_by('maxpayout').last()

    #winch 3 casts calculations
    casts_winch3=casts.filter(winch='1')
    casts_winch3_count=casts_winch3.count()
    casts_winch3_maxtension=casts_winch3.order_by('maxtension').last()
    casts_winch3_maxpayout=casts_winch3.order_by('maxpayout').last()

    context ={
        'cruise':cruise,
        'casts': casts,
        'winch1' : winch1,
        'winch2' : winch2,
        'winch3' : winch3,
        'casts_winch1_maxtension':casts_winch1_maxtension,
        'casts_winch1_maxpayout':casts_winch1_maxpayout,
        'casts_winch1_count':casts_winch1_count,
        'casts_winch2_maxtension':casts_winch2_maxtension,
        'casts_winch2_maxpayout':casts_winch2_maxpayout,
        'casts_winch2_count':casts_winch2_count,
        'casts_winch3_maxtension':casts_winch3_maxtension,
        'casts_winch3_maxpayout':casts_winch3_maxpayout,
        'casts_winch3_count':casts_winch3_count,
        }

    return render(request, "wwdb/reports/cruisereport.html", context)

def cruise_report_file(request, pk):

    response = HttpResponse(content_type="text/plain")
    response['Content-Disposition']='attachement; filename=cruise_report.txt'
    
    #cruise object and casts by cruise daterange
    cruise=Cruise.objects.filter(id=pk)
    cruise_object=cruise.last()
    startdate=cruise_object.startdate
    enddate=cruise_object.enddate
    casts=Cast.objects.filter(startdate__range=[startdate, enddate])

    #winch status objects
    winch1=cruise_object.winch1
    winch2=cruise_object.winch2
    winch3=cruise_object.winch3

    #winch 1 casts calculations
    casts_winch1=casts.filter(winch='3')
    casts_winch1_count=casts_winch1.count()
    casts_winch1_maxtension=casts_winch1.order_by('maxtension').last()
    casts_winch1_maxpayout=casts_winch1.order_by('maxpayout').last()

    #winch 2 casts calculations
    casts_winch2=casts.filter(winch='2')
    casts_winch2_count=casts_winch2.count()
    casts_winch2_maxtension=casts_winch2.order_by('maxtension').last()
    casts_winch2_maxpayout=casts_winch2.order_by('maxpayout').last()

    #winch 3 casts calculations
    casts_winch3=casts.filter(winch='1')
    casts_winch3_count=casts_winch3.count()
    casts_winch3_maxtension=casts_winch3.order_by('maxtension').last()
    casts_winch3_maxpayout=casts_winch3.order_by('maxpayout').last()    

    lines = []
    lines.append(cruise_object.number)

    if casts_winch1_maxtension:
        lines.append('\nWinch 1\nMax tension: ' + str(casts_winch1_maxtension.maxtension) + 
                     'lbs\nMax payout: ' + str(casts_winch1_maxpayout.maxpayout) + 
                     'm\nNumber of casts: ' + str(casts_winch1_count) +
                     '\nBlock arrangement: ' + cruise_object.winch1blockarrangement + 
                     '\nTermination: ' + cruise_object.winch1termination +
                     '\nNotes: ' + cruise_object.winch1notes)
    else:
        lines.append('\n\n\nWinch 1 not used')

    if casts_winch2_maxtension:
        lines.append('\n\n\nWinch 2\nMax tension: ' + str(casts_winch2_maxtension.maxtension) + 
                        'lbs\nMax payout: ' + str(casts_winch2_maxpayout.maxpayout) + 
                        'm\nNumber of casts: ' + str(casts_winch2_count) +
                        '\nBlock arrangement: ' + cruise_object.winch2blockarrangement + 
                        '\nTermination: ' + cruise_object.winch2termination +
                        '\nSpin direction: ' + cruise.object.winch2spindirection +
                        '\nNotes: ' + cruise_object.winch2notes)
    else:
        lines.append('\n\n\nWinch 2 not used')

    if casts_winch3_maxtension:
        lines.append('\n\n\nWinch 3\nMax tension: ' + str(casts_winch3_maxtension.maxtension) + 
                     'lbs\nMax payout: ' + str(casts_winch3_maxpayout.maxpayout) + 
                     'm\nNumber of casts: ' + str(casts_winch3_count) + 
                     '\nBlock arrangement: ' + cruise_object.winch3blockarrangement + 
                     '\nTermination: ' + cruise_object.winch3termination +
                     '\nNotes: ' + cruise_object.winch3notes)

    else:
        lines.append('\n\n\nWinch 3 not used')

    response.writelines(lines)

    return response

def wiredrumlist(request):
    wire_drum = Wiredrum.objects.order_by('-date')

    context = {
        'wire_drum': wire_drum, 
        }

    return render(request, 'wwdb/inventories/wiredrumlist.html', context=context)

def wiredrumedit(request, id):
    context ={}
    obj = get_object_or_404(Wiredrum, id = id)

    if request.method == 'POST':
        form = EditWireDrumForm(request.POST, instance = obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/wwdb/inventories/wiredrumlist')
    else:
        form = EditWireDrumForm(instance = obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/wwdb/inventories/wiredrum/%i/edit' % wiredrumid.pk)

    context["form"] = form
    return render(request, "wwdb/inventories/wiredrumedit.html", context)

def wiredrumadd(request):
    context ={}
    form = WireDrumAddForm(request.POST or None)
    if request.method == "POST":
        form = WireDrumAddForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/wwdb/inventories/wiredrumlist')
    else:
        form = WireDrumAddForm 
        if 'submitted' in request.GET:
            submitted = True
            return render(request, 'wwdb/inventories/wiredrumadd.html', {'form':form, 'submitted':submitted, 'id':id})
 
    context['form']= form

    return render(request, "wwdb/inventories/wiredrumadd.html", context)

def drumlocationedit(request, id):
    context ={}
    obj = get_object_or_404(DrumLocation, id = id)

    if request.method == 'POST':
        form = EditDrumLocationForm(request.POST, instance = obj)
        if form.is_valid():
            form.save()
            obj.retain_wire_length()
            obj.save()
            drumlocation=DrumLocation.objects.get(id=id)
            return HttpResponseRedirect('/wwdb/inventories/drumlocationlist')
    else:
        form = EditDrumLocationForm(instance = obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/wwdb/inventories/drumlocation/%i/edit' % drumlocationid.pk)

    context["form"] = form
    return render(request, "wwdb/inventories/drumlocationedit.html", context)

def drumlocationadd(request):
    context ={}
    form = DrumLocationAddForm(request.POST or None)
    if request.method == "POST":
        form = DrumLocationAddForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            obj=DrumLocation.objects.last()
            obj.retain_wire_length()
            obj.save()
            return HttpResponseRedirect('/wwdb/inventories/drumlocationlist')
    else:
        form = DrumLocationAddForm 
        if 'submitted' in request.GET:
            submitted = True
            return render(request, 'wwdb/inventories/drumlocationadd.html', {'form':form, 'submitted':submitted, 'id':id})
 
    context['form']= form

    return render(request, "wwdb/inventories/drumlocationadd.html", context)

def drumlocationlist(request):
    drum_location = DrumLocation.objects.order_by('-date')
    
    context = {
        'drum_location': drum_location,
        }

    return render(request, 'wwdb/inventories/drumlocationlist.html', context=context)


def castplot(request, pk):

    obj = get_object_or_404(Cast, id=pk)

    conn = pyodbc.connect('Driver={SQL Server};'
                            'Server=192.168.1.90, 1433;'
                            'Database=WinchDb;'
                            'Trusted_Connection=no;'
			        'UID=remoteadmin;'
			        'PWD=eris.2003;')

    winch=(obj.winch.name)
    startcal=str(obj.startdate)
    endcal=str(obj.enddate)

    df=pd.read_sql_query("SELECT * FROM " + winch + " WHERE DateTime BETWEEN '" + startcal + "' AND '" + endcal + "'", conn)

    df_tension_datetime=df.loc[:,['DateTime','Tension','Payout']]
    df_json=df_tension_datetime.to_json(orient='records')

    return render(request, 'wwdb/reports/castplot.html', {'df_json': df_json})


"""
Postings
"""

def safeworkingtensions(request):
    active_wire = Wire.objects.filter(status=True).order_by('-winch')

    context = {
        'active_wire': active_wire,
        }

    return render(request, 'wwdb/reports/safeworkingtensions.html', context=context)

"""
Maintenance
"""


def wirelist(request):
    wires_in_use = Wire.objects.filter(status=True)
    wires_in_storage = Wire.objects.filter(status=False)
    wires = Wire.objects.all()
    drums=Drum.objects.all()
    
    context = {
        'wires_in_use': wires_in_use,
        'wires_in_storage': wires_in_storage, 
        'wires' : wires,
        'drums' : drums,
        }

    return render(request, 'wwdb/inventories/wirelist.html', context=context)

"""
WIRES
Classes related to create, update, view Wire model
"""

class WireDetail(DetailView):
    model = Wire
    template_name="wwdb/inventories/wiredetail.html"

class WireEdit(UpdateView):
    model = Wire
    template_name="wwdb/inventories/wireedit.html"
    fields=['wirerope','manufacturerid','nsfid','dateacquired','notes','status','factorofsafety']
    
    def get_form(self):
        form = super().get_form()
        form.fields['dateacquired'].widget = DateTimePickerInput()
        return form

class WireAdd(CreateView):
    model = Wire
    template_name="wwdb/inventories/wireadd.html"
    fields=['wireropeid','manufacturerid','nsfid','dateacquired','notes','length','status']

"""
WINCHES
Classes related to create, update, view Winch model
"""

class WinchList(ListView):
    model = Winch
    template_name="wwdb/inventories/winchlist.html"

class WinchDetail(DetailView):
    model = Winch
    template_name="wwdb/inventories/winchdetail.html"

class WinchEdit(UpdateView):
    model = Winch
    template_name="wwdb/inventories/winchedit.html"
    fields=['locationid','ship','institution','manufacturer']

def wincheditstatus(request, id):
    context ={}
    obj = get_object_or_404(Winch, id = id)

    if request.method == 'POST':
        form = EditWinchStatusForm(request.POST, instance = obj)
        if form.is_valid():
            form.save()
            winchid=Winch.objects.get(id=id)
            return HttpResponseRedirect("/wwdb/configuration/cruiseconfiguration")
    else:
        form = EditWinchStatusForm(instance = obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/wwdb/inventories/winch/%i/editstatus" % winchid.pk)

    context["form"] = form
    return render(request, "wwdb/inventories/wincheditstatus.html", context)

def winchadd(request):
    context ={}
    form = WinchAddForm(request.POST or None)
    if request.method == "POST":
        form = WinchAddForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/wwdb/configuration/cruiseconfiguration')
    else:
        form = WinchAddForm 
        if 'submitted' in request.GET:
            submitted = True
            return render(request, 'wwdb/inventories/winchadd.html', {'form':form, 'submitted':submitted, 'id':id})
 
    context['form']= form

    return render(request, "wwdb/inventories/winchadd.html", context)

"""
WINCH OPERATORS
Classes related to create, update, view WinchOperators model
"""

class OperatorList(ListView):
    model = WinchOperator
    template_name="wwdb/configuration/operatorlist.html"

class OperatorDetail(DetailView):
    model = WinchOperator
    template_name="wwdb/configuration/operatordetail.html"

class OperatorEdit(UpdateView):
    model = WinchOperator
    template_name="wwdb/configuration/operatoredit.html"
    fields=['username','firstname','lastname','status']


def operatoreditstatus(request, id):
    context ={}
    obj = get_object_or_404(WinchOperator, id = id)

    if request.method == 'POST':
        form = EditOperatorStatusForm(request.POST, instance = obj)
        if form.is_valid():
            form.save()
            operatorid=WinchOperator.objects.get(id=id)
            return HttpResponseRedirect("/wwdb/configuration/cruiseconfiguration")
    else:
        form = EditOperatorStatusForm(instance = obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/wwdb/configuration/operator/%i/editstatus" % operatorid.pk)

    context["form"] = form
    return render(request, "wwdb/configuration/operatoreditstatus.html", context)

class OperatorAdd(CreateView):
    model = WinchOperator
    template_name="wwdb/configuration/operatoradd.html"
    fields=['username','firstname','lastname','status']

def operatoradd(request):
    context ={}
    form = AddOperatorForm(request.POST or None)
    if request.method == "POST":
        form = AddOperatorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/wwdb/configuration/cruiseconfiguration")
    else:
        form = AddOperatorForm 
        if 'submitted' in request.GET:
            submitted = True
            return render(request, 'wwdb/configuration/operatoradd.html', {'form':form, 'submitted':submitted, 'id':id})

    context['form']= form

    return render(request, 'wwdb/configuration/deploymentadd.html', context)

"""
DEPLOYMENTS 
Classes related to create, update, view DeploymentType model
"""

class DeploymentList(ListView):
    model = DeploymentType
    template_name="wwdb/configuration/deploymentlist.html"

class DeploymentDetail(DetailView):
    model = DeploymentType
    template_name="wwdb/configuration/deploymentdetail.html"

class DeploymentEdit(UpdateView):
    model = DeploymentType
    template_name="wwdb/configuration/deploymentedit.html"
    fields=['name','equipment','notes','status']


def deploymenteditstatus(request, id):
    context ={}
    obj = get_object_or_404(DeploymentType, id = id)

    if request.method == 'POST':
        form = EditDeploymentStatusForm(request.POST, instance = obj)
        if form.is_valid():
            form.save()
            deploymentid=DeploymentType.objects.get(id=id)
            return HttpResponseRedirect("/wwdb/configuration/cruiseconfiguration")
    else:
        form = EditDeploymentStatusForm(instance = obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/wwdb/configuration/deployment/%i/editstatus" % deploymenttypeid.pk)

    context["form"] = form
    return render(request, "wwdb/configuration/deploymenteditstatus.html", context)

def deploymentadd(request):
    context ={}
    form = AddDeploymentForm(request.POST or None)
    if request.method == "POST":
        form = AddDeploymentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/wwdb/configuration/cruiseconfiguration")
    else:
        form = AddDeploymentForm 
        if 'submitted' in request.GET:
            submitted = True
            return render(request, 'wwdb/configuration/deploymentadd.html', {'form':form, 'submitted':submitted, 'id':id})

    context['form']= form

    return render(request, 'wwdb/configuration/deploymentadd.html', context)


def breaktestlist(request):
    break_test = Breaktest.objects.order_by('-date')

    context = {
        'break_test': break_test, 
        }

    return render(request, 'wwdb/maintenance/breaktestlist.html', context=context)

"""
CUTBACKRETERMINATION
Classes related to create, update, view CutbackRetermination model
"""

def cutbackreterminationlist(request):
    cutbacks_reterminations = CutbackRetermination.objects.order_by('-date')

    context = {
        'cutbacks_reterminations': cutbacks_reterminations, 
        }

    return render(request, 'wwdb/maintenance/cutbackreterminationlist.html', context=context)


def cutbackreterminationedit(request, id):
    context ={}
    obj = get_object_or_404(CutbackRetermination, id = id)

    if request.method == 'POST':
        form = EditCutbackReterminationForm(request.POST, instance = obj)
        if form.is_valid():
            form.save()
            obj.submitlength()
            obj.save()
            return HttpResponseRedirect('/wwdb/maintenance/cutbackreterminationlist')
    else:
        form = EditCutbackReterminationForm(instance = obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/wwdb/maintenance/cutbackretermination/%i/edit" % cutbackreterminationid.pk)

    context["form"] = form
    return render(request, "wwdb/maintenance/cutbackreterminationedit.html", context)


class CutbackReterminationDetail(DetailView):
    model = CutbackRetermination
    template_name="wwdb/maintenance/cutbackreterminationdetail.html"

class CutbackReterminationAdd(CreateView):
    model = CutbackRetermination
    template_name="wwdb/maintenance/cutbackreterminationadd.html"
    fields=['dryendtag','wetendtag', 'lengthremoved','wireid','date','notes']

def cutbackreterminationadd(request):
    context ={}
    form = AddCutbackReterminationForm(request.POST or None)
    if request.method == "POST":
        form = AddCutbackReterminationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            obj=CutbackRetermination.objects.last()
            obj.submitlength()
            obj.save()
            return HttpResponseRedirect("/wwdb/maintenance/cutbackreterminationlist")
    else:
        form = AddCutbackReterminationForm 
        if 'submitted' in request.GET:
            submitted = True
            return render(request, 'wwdb/maintenance/cutbackreterminationadd.html', {'form':form, 'submitted':submitted, 'id':id})

    context['form']= form

    return render(request, 'wwdb/maintenance/cutbackreterminationadd.html', context)


"""
DRUM
Classes related to create, update, view Drum model
"""

def drumlist(request):
    drum_list = Drum.objects.order_by('internalid')

    context = {
        'drum_list': drum_list, 
        }

    return render(request, 'wwdb/inventories/drumlist.html', context=context)

def drumedit(request, id):
    context ={}
    obj = get_object_or_404(Drum, id = id)

    if request.method == 'POST':
        form = EditDrumForm(request.POST, instance = obj)
        if form.is_valid():
            form.save()
            drum=Drum.objects.get(id=id)
            return HttpResponseRedirect('/wwdb/inventories/drumlist')
    else:
        form = EditDrumForm(instance = obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/wwdb/inventories/drum/%i/edit" % drumid.pk)

    context["form"] = form
    return render(request, "wwdb/inventories/drumedit.html", context)

class DrumDetail(DetailView):
    model = Drum
    template_name="wwdb/inventories/drumdetail.html"

def drumadd(request):
    context ={}
    form = AddDrumForm(request.POST or None)
    if request.method == "POST":
        form = AddDrumForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/wwdb/inventories/drumlist")
    else:
        form = AddDrumForm 
        if 'submitted' in request.GET:
            submitted = True
            return render(request, 'wwdb/inventories/drumadd.html', {'form':form, 'submitted':submitted, 'id':id})

    context['form']= form

    return render(request, 'wwdb/inventories/drumadd.html', context)

"""
Cruises
Classes related to create, update, view Cruise model
"""

def cruiseedit(request, id):
    context ={}
    obj = get_object_or_404(Cruise, id = id)

    if request.method == 'POST':
        form = EditCruiseForm(request.POST, instance = obj)
        if form.is_valid():
            form.save()
            cruiseid=Cruise.objects.get(id=id)
            return HttpResponseRedirect("/wwdb/configuration/cruiseconfiguration")
    else:
        form = EditCruiseForm(instance = obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/wwdb/configuration/cruise/%i/edit" % cruiseid.pk)

    context["form"] = form
    return render(request, "wwdb/configuration/cruiseedit.html", context)

def cruiseadd(request):
    context ={}
    form = CruiseAddForm(request.POST or None)
    if request.method == "POST":
        form = CruiseAddForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/wwdb/configuration/cruiseconfiguration")
    else:
        form = CruiseAddForm 
        if 'submitted' in request.GET:
            submitted = True
            return render(request, 'wwdb/configuration/cruiseadd.html', {'form':form, 'submitted':submitted, 'id':id})

    context['form']= form

    return render(request, 'wwdb/configuration/cruiseadd.html', context)


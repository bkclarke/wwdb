from django import template
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from .models import *
from django.views.generic import *
from django.urls import reverse_lazy
from django.urls import reverse
from bootstrap_datepicker_plus import *
from .forms import *
from django.shortcuts import render, get_object_or_404
import pandas as pd
from django.db.models import Count
import pyodbc 
from django.db.models import Avg, Count, Min, Sum, Max
import logging

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
            return render(request, 'wwdb/caststart.html', {'form':form, 'submitted':submitted, 'id':id})

    context['form']= form

    return render(request, "wwdb/caststart.html", context)

def castlist(request):
    cast_noflag = Cast.objects.filter(flagforreview=False, maxpayout__isnull=False, payoutmaxtension__isnull=False, maxtension__isnull=False)
    cast_flag = Cast.objects.filter(flagforreview=True)|Cast.objects.filter(maxpayout__isnull=True)|Cast.objects.filter(payoutmaxtension__isnull=True)|Cast.objects.filter(maxtension__isnull=True)

    context = {
        'cast_noflag': cast_noflag,
        'cast_flag': cast_flag,
       }

    return render(request, 'wwdb/castlist.html', context=context)

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
            return HttpResponseRedirect("/wwdb/cast/%i/castenddetail" % cast.pk)
    context["form"] = form
    return render(request, "wwdb/castend.html", context)

def castedit(request, id):
    context ={}
    obj = Cast.objects.get(id=id)
    if request.method == 'POST':
        form = EditCastForm(request.POST, instance = obj)
        if form.is_valid():
            form.save()
            obj.endcastcal()
            obj.save()
            return HttpResponseRedirect('/wwdb/castlist')
    else:
        form = EditCastForm(instance = obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/wwdb/cast/%i/edit' % cast.pk)

    context["form"] = form
    return render(request, "wwdb/castedit.html", context)

def castdetail(request, id):
    context ={}
    context["cast"] = Cast.objects.get(id = id)     
    return render(request, "wwdb/castdetail.html", context)

class CastDelete(DeleteView):
    model = Cast
    template_name="wwdb/castdelete.html"
    success_url= reverse_lazy('home')

def castenddetail(request, id):
    context ={}
    context["cast"] = Cast.objects.get(id = id)
    return render(request, "wwdb/castenddetail.html", context)

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

    return render(request, 'wwdb/cruiseconfigurehome.html', context=context)

def wireeditfactorofsafety(request, id):
    context ={}
    obj = get_object_or_404(Wire, id = id)

    if request.method == 'POST':
        form = EditFactorofSafetyForm(request.POST, instance = obj)
        if form.is_valid():
            form.save()
            wireid=Wire.objects.get(id=id)
            return HttpResponseRedirect("/wwdb/cruiseconfigurehome")
    else:
        form = EditFactorofSafetyForm(instance = obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/wwdb/wire/%i/editfactorofsafety" % wireid.pk)

    context["form"] = form
    return render(request, "wwdb/wireeditfactorofsafety.html", context)


"""
WINCH WIRE REPORTING
Classes related to winch and wire reporting 
"""

def reportinghome(request):
    cutbacks_retermination = CutbackRetermination.objects.order_by('-date')
    break_test = Breaktest.objects.order_by('-date')
    wire_drum = Wiredrum.objects.order_by('-date')
    drum_location = DrumLocation.objects.order_by('-date')

    context = {
        'cutbacks_reterminations': cutbacks_retermination, 
        'break_test': break_test,
        'wire_drum': wire_drum, 
        'drum_location':drum_location,
        }

    return render(request, 'reports/reporting.html', context=context)

def highchart(request):
    return render(request, 'wwdb/highchart.html')

"""
def highchart(request, id):

    obj = get_object_or_404(Cast, id = id)

    conn = pyodbc.connect('Driver={SQL Server};'
                            'Server=192.168.2.5, 1433;'
                            'Database=WinchDb;'
                            'Trusted_Connection=no;'
			        'UID=remoteadmin;'
			        'PWD=eris.2003;')

    winch=(obj.winch.name)
    startcal=str(obj.startdate)
    endcal=str(obj.enddate)

    df=pd.read_sql_query("SELECT * FROM " + winch + " WHERE DateTime BETWEEN '" + startcal + "' AND '" + endcal + "'", conn)

    tension=df['Tension']
    datetime=df['DateTime']
    context = {
        'tension': tension,
        'datetime': datetime,
        }

    return render(request, 'wwdb/highchart.html', context=context)
"""

def cruisereport(request):
    cruise_id=Cruise.objects.filter(status=True).first()
    cruise = Cruise.objects.filter(status=True)
    operators = WinchOperator.objects.filter(status=True)
    active_wire = Wire.objects.filter(status=True)
    winches = Winch.objects.filter(status=True)
    casts = Cast.objects.filter(cruisenumber=cruise_id)

    deployments = DeploymentType.objects.filter(cast__in=casts)
    deployments = DeploymentType.objects.filter(cast__in=casts).annotate(num_casts=Count('id'))

    context = {
        'operators': operators,
        'deployments': deployments,
        'active_wire': active_wire,
        'winches': winches,
        'cruise' : cruise,
        'casts' : casts,
       }

    return render(request, 'reports/cruisereport.html', context=context)


#def wiredrumadd(request):

def wiredrumlist(request):
    wire_drum = Wiredrum.objects.order_by('-date')

    context = {
        'wire_drum': wire_drum, 
        }

    return render(request, 'reports/wiredrumlist.html', context=context)

def wiredrumedit(request, id):
    context ={}
    obj = get_object_or_404(Wiredrum, id = id)

    if request.method == 'POST':
        form = EditWireDrumForm(request.POST, instance = obj)
        if form.is_valid():
            form.save()
            wiredrum=Wiredrum.objects.get(id=id)
            return HttpResponseRedirect('/wwdb/reports/wiredrumlist')
    else:
        form = EditWireDrumForm(instance = obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/wwdb/wiredrum/%i/edit' % wiredrumid.pk)

    context["form"] = form
    return render(request, "wwdb/wiredrumedit.html", context)

def wiredrumadd(request):
    context ={}
    form = WireDrumAddForm(request.POST or None)
    if request.method == "POST":
        form = WireDrumAddForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/wwdb/reports/wiredrumlist')
    else:
        form = WireDrumAddForm 
        if 'submitted' in request.GET:
            submitted = True
            return render(request, 'wwdb/wiredrumadd.html', {'form':form, 'submitted':submitted, 'id':id})
 
    context['form']= form

    return render(request, "wwdb/wiredrumadd.html", context)


def drumlocationadd(request):
    context ={}
    form = DrumLocationAddForm(request.POST or None)
    if request.method == "POST":
        form = DrumLocationAddForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/wwdb/reports')
    else:
        form = DrumLocationAddForm 
        if 'submitted' in request.GET:
            submitted = True
            return render(request, 'wwdb/drumlocationadd.html', {'form':form, 'submitted':submitted, 'id':id})
 
    context['form']= form

    return render(request, "wwdb/drumlocationadd.html", context)
"""
Postings
"""

def safeworkingtensions(request):
    active_wire = Wire.objects.filter(status=True).order_by('-winch')

    context = {
        'active_wire': active_wire,
        }

    return render(request, 'reports/safeworkingtensions.html', context=context)

"""
Movements
"""


"""
Maintenance
"""


def inventories(request):
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

    return render(request, 'reports/inventories.html', context=context)

"""
WIRES
Classes related to create, update, view Wire model
"""

class WireList(ListView):
    model = Wire
    template_name="wwdb/wirelist.html"

class WireDetail(DetailView):
    model = Wire
    template_name="wwdb/wiredetail.html"

class WireEdit(UpdateView):
    model = Wire
    template_name="wwdb/wireedit.html"
    fields=['wirerope','manufacturerid','nsfid','dateacquired','notes','status','factorofsafety']
    
    def get_form(self):
        form = super().get_form()
        form.fields['dateacquired'].widget = DateTimePickerInput()
        return form

class WireAdd(CreateView):
    model = Wire
    template_name="wwdb/wireadd.html"
    fields=['wireropeid','manufacturerid','nsfid','dateacquired','notes','length','status']

"""
WINCHES
Classes related to create, update, view Winch model
"""

class WinchList(ListView):
    model = Winch
    template_name="wwdb/winchlist.html"

class WinchDetail(DetailView):
    model = Winch
    template_name="wwdb/winchdetail.html"

class WinchEdit(UpdateView):
    model = Winch
    template_name="wwdb/winchedit.html"
    fields=['locationid','ship','institution','manufacturer']

def wincheditstatus(request, id):
    context ={}
    obj = get_object_or_404(Winch, id = id)

    if request.method == 'POST':
        form = EditWinchStatusForm(request.POST, instance = obj)
        if form.is_valid():
            form.save()
            winchid=Winch.objects.get(id=id)
            return HttpResponseRedirect("/wwdb/cruiseconfigurehome")
    else:
        form = EditWinchStatusForm(instance = obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/wwdb/winch/%i/editstatus" % winchid.pk)

    context["form"] = form
    return render(request, "wwdb/wincheditstatus.html", context)

class WinchAdd(CreateView):
    model = Winch
    template_name="wwdb/winchadd.html"
    fields=['locationid','ship','institution','manufacturer']

"""
WINCH OPERATORS
Classes related to create, update, view WinchOperators model
"""

class OperatorList(ListView):
    model = WinchOperator
    template_name="wwdb/operatorlist.html"

class OperatorDetail(DetailView):
    model = WinchOperator
    template_name="wwdb/operatordetail.html"

class OperatorEdit(UpdateView):
    model = WinchOperator
    template_name="wwdb/operatoredit.html"
    fields=['username','firstname','lastname','status']


def operatoreditstatus(request, id):
    context ={}
    obj = get_object_or_404(WinchOperator, id = id)

    if request.method == 'POST':
        form = EditOperatorStatusForm(request.POST, instance = obj)
        if form.is_valid():
            form.save()
            operatorid=WinchOperator.objects.get(id=id)
            return HttpResponseRedirect("/wwdb/cruiseconfigurehome")
    else:
        form = EditOperatorStatusForm(instance = obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/wwdb/operator/%i/editstatus" % operatorid.pk)

    context["form"] = form
    return render(request, "wwdb/operatoreditstatus.html", context)

class OperatorAdd(CreateView):
    model = WinchOperator
    template_name="wwdb/operatoradd.html"
    fields=['username','firstname','lastname','status']

def operatoradd(request):
    context ={}
    form = AddOperatorForm(request.POST or None)
    if request.method == "POST":
        form = AddOperatorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/wwdb/cruiseconfigurehome")
    else:
        form = AddOperatorForm 
        if 'submitted' in request.GET:
            submitted = True
            return render(request, 'wwdb/operatoradd.html', {'form':form, 'submitted':submitted, 'id':id})

    context['form']= form

    return render(request, 'wwdb/deploymentadd.html', context)

"""
DEPLOYMENTS 
Classes related to create, update, view DeploymentType model
"""

class DeploymentList(ListView):
    model = DeploymentType
    template_name="wwdb/deploymentlist.html"

class DeploymentDetail(DetailView):
    model = DeploymentType
    template_name="wwdb/deploymentdetail.html"

class DeploymentEdit(UpdateView):
    model = DeploymentType
    template_name="wwdb/deploymentedit.html"
    fields=['name','equipment','notes','status']


def deploymenteditstatus(request, id):
    context ={}
    obj = get_object_or_404(DeploymentType, id = id)

    if request.method == 'POST':
        form = EditDeploymentStatusForm(request.POST, instance = obj)
        if form.is_valid():
            form.save()
            deploymentid=DeploymentType.objects.get(id=id)
            return HttpResponseRedirect("/wwdb/cruiseconfigurehome")
    else:
        form = EditDeploymentStatusForm(instance = obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/wwdb/deployment/%i/editstatus" % deploymenttypeid.pk)

    context["form"] = form
    return render(request, "wwdb/deploymenteditstatus.html", context)

def deploymentadd(request):
    context ={}
    form = AddDeploymentForm(request.POST or None)
    if request.method == "POST":
        form = AddDeploymentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/wwdb/cruiseconfigurehome")
    else:
        form = AddDeploymentForm 
        if 'submitted' in request.GET:
            submitted = True
            return render(request, 'wwdb/deploymentadd.html', {'form':form, 'submitted':submitted, 'id':id})

    context['form']= form

    return render(request, 'wwdb/deploymentadd.html', context)


def breaktestlist(request):
    break_test = Breaktest.objects.order_by('-date')

    context = {
        'break_test': break_test, 
        }

    return render(request, 'reports/breaktestlist.html', context=context)

"""
CUTBACKRETERMINATION
Classes related to create, update, view CutbackRetermination model
"""

def cutbackreterminationlist(request):
    cutbacks_reterminations = CutbackRetermination.objects.order_by('-date')

    context = {
        'cutbacks_reterminations': cutbacks_reterminations, 
        }

    return render(request, 'reports/cutbackreterminationlist.html', context=context)

def cutbackreterminationedit(request, id):
    context ={}
    obj = get_object_or_404(CutbackRetermination, id = id)

    if request.method == 'POST':
        form = EditCutbackReterminationForm(request.POST, instance = obj)
        if form.is_valid():
            form.save()
            cutbackretermination=CutbackRetermination.objects.get(id=id)
            return HttpResponseRedirect('/wwdb/reports/cutbackreterminationlist')
    else:
        form = EditCutbackReterminationForm(instance = obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/wwdb/cutbackretermination/%i/edit" % cutbackreterminationid.pk)

    context["form"] = form
    return render(request, "wwdb/cutbackreterminationedit.html", context)


class CutbackReterminationDetail(DetailView):
    model = CutbackRetermination
    template_name="wwdb/cutbackreterminationdetail.html"

class CutbackReterminationAdd(CreateView):
    model = CutbackRetermination
    template_name="wwdb/cutbackreterminationadd.html"
    fields=['dryendtag','wetendtag', 'lengthremoved','wireid','date','notes']

def cutbackreterminationadd(request):
    context ={}
    form = AddCutbackReterminationForm(request.POST or None)
    if request.method == "POST":
        form = AddCutbackReterminationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/wwdb/reports/cutbackreterminationlist")
    else:
        form = AddCutbackReterminationForm 
        if 'submitted' in request.GET:
            submitted = True
            return render(request, 'wwdb/cutbackreterminationadd.html', {'form':form, 'submitted':submitted, 'id':id})

    context['form']= form

    return render(request, 'wwdb/cutbackreterminationadd.html', context)

"""
DRUM
Classes related to create, update, view Drum model
"""

def drumlist(request):
    drum_list = Drum.objects.order_by('internalid')

    context = {
        'drum_list': drum_list, 
        }

    return render(request, 'reports/drumlist.html', context=context)

def drumedit(request, id):
    context ={}
    obj = get_object_or_404(Drum, id = id)

    if request.method == 'POST':
        form = EditDrumForm(request.POST, instance = obj)
        if form.is_valid():
            form.save()
            drum=Drum.objects.get(id=id)
            return HttpResponseRedirect('/wwdb/reports/drumlist')
    else:
        form = EditDrumForm(instance = obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/wwdb/drum/%i/edit" % drumid.pk)

    context["form"] = form
    return render(request, "wwdb/drumedit.html", context)

class DrumDetail(DetailView):
    model = Drum
    template_name="wwdb/drumdetail.html"

def drumadd(request):
    context ={}
    form = AddDrumForm(request.POST or None)
    if request.method == "POST":
        form = AddDrumForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/wwdb/reports/drumlist")
    else:
        form = AddDrumForm 
        if 'submitted' in request.GET:
            submitted = True
            return render(request, 'wwdb/drumadd.html', {'form':form, 'submitted':submitted, 'id':id})

    context['form']= form

    return render(request, 'wwdb/drumadd.html', context)

"""
Cruises
Classes related to create, update, view Cruise model
"""

def cruiseeditstatus(request, id):
    context ={}
    obj = get_object_or_404(Cruise, id = id)

    if request.method == 'POST':
        form = EditCruiseForm(request.POST, instance = obj)
        if form.is_valid():
            form.save()
            cruiseid=Cruise.objects.get(id=id)
            return HttpResponseRedirect("/wwdb/cruiseconfigurehome")
    else:
        form = EditCruiseForm(instance = obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/wwdb/cruise/%i/editstatus" % cruiseid.pk)

    context["form"] = form
    return render(request, "wwdb/cruiseeditstatus.html", context)

def cruiseadd(request):
    context ={}
    form = CruiseAddForm(request.POST or None)
    if request.method == "POST":
        form = CruiseAddForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/wwdb/cruiseconfigurehome")
    else:
        form = CruiseAddForm 
        if 'submitted' in request.GET:
            submitted = True
            return render(request, 'wwdb/cruiseadd.html', {'form':form, 'submitted':submitted, 'id':id})

    context['form']= form

    return render(request, 'wwdb/cruiseadd.html', context)

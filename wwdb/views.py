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

def home(request):
    template = loader.get_template('wwdb/home.html')
    context = {}
    return HttpResponse(template.render(context, request))

"""
CASTS
Classes related to create, update, delete, view Cast model
"""

class CastList(ListView):
    model = Cast
    template_name="wwdb/castlist.html"

def castlist(request):
    cast_noflag = Cast.objects.filter(flagforreview=False, maxpayout__isnull=False, payoutmaxtension__isnull=False, maxtension__isnull=False)
    cast_flag = Cast.objects.filter(flagforreview=True)|Cast.objects.filter(maxpayout__isnull=True)|Cast.objects.filter(payoutmaxtension__isnull=True)|Cast.objects.filter(maxtension__isnull=True)

    context = {
        'cast_noflag': cast_noflag,
        'cast_flag': cast_flag,
       }

    return render(request, 'wwdb/castlist.html', context=context)

def castedit(request, id):
    context ={}
    obj = get_object_or_404(Cast, id = id)

    if request.method == 'POST':
        form = EditCastForm(request.POST, instance = obj)
        if form.is_valid():
            form.save()
            cast=Cast.objects.get(id=id)
            return HttpResponseRedirect('/wwdb/castlist')
    else:
        form = EditCastForm(instance = obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/wwdb/cast/%i/edit' % castid.pk)

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

"""
CASTS
Classes related to starting and ending a cast, viewing and updating after ending a cast, Cast model
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

def castenddetail(request, id):
    context ={}
    context["cast"] = Cast.objects.get(id = id)
    return render(request, "wwdb/castenddetail.html", context)
               
def castend(request, id):
    context ={}
    obj = get_object_or_404(Cast, id = id)
    form = EndCastForm(request.POST or None, instance = obj)
    try:
        if form.is_valid():
            form.save()
            castid=Cast.objects.last()
            castid.endcastcal()
            castid.save()
            return HttpResponseRedirect("/wwdb/cast/%i/castenddetail" % castid.pk)
 
        context["form"] = form
        return render(request, "wwdb/castend.html", context)

    except:
        if form.is_valid():
            form.save()
            castid=Cast.objects.last()
            return HttpResponseRedirect("/wwdb/cast/%i/castenddetail" % castid.pk)
 
        context["form"] = form
        return render(request, "wwdb/castend.html", context)


"""
PRECRUISE CONFIGURATION
Classes related to starting a cruise including updating WinchOperators and DeploymentType models
"""

def cruiseconfigurehome(request):
    operators = WinchOperator.objects.all()
    deployments = DeploymentType.objects.all()
    active_wire = Wire.objects.filter(status=True)
    winches = Winch.objects.all()

    context = {
        'operators': operators,
        'deployments': deployments,
        'active_wire': active_wire,
        'winches': winches,
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
    return render(request, 'reports/reporting.html')

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


def wireinventory(request):
    wires_in_use = Wire.objects.filter(status=True)
    wires_in_storage = Wire.objects.filter(status=False)
    wires = Wire.objects.all()
    
    context = {
        'wires_in_use': wires_in_use,
        'wires_in_storage': wires_in_storage, 
        'wires' : wires,
        }

    return render(request, 'reports/wireinventory.html', context=context)

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
    fields=['wireropeid','manufacturerid','nsfid','dateacquired','notes','status','factorofsafety']
    
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

class DeploymentAdd(CreateView):
    model = DeploymentType
    template_name="wwdb/deploymentadd.html"
    fields=['name','equipment','notes','status']

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


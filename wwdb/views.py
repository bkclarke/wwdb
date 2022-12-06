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

def castedit(request, id):
    context ={}
    obj = get_object_or_404(Cast, id = id)
    form = EditCastForm(request.POST or None, instance = obj)
 
    if form.is_valid():
        form.save()
        castid=Cast.objects.get(id = id)
        return HttpResponseRedirect("/wwdb/cast/%i/edit" % castid.pk)
 
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
    context = {
        'operators': operators,
        'deployments': deployments,
       }

    return render(request, 'wwdb/cruiseconfigurehome.html', context=context)

"""
WINCH WIRE REPORTING
Classes related to winch and wire reporting 
"""

def reportinghome(request):
    return render(request, 'reports/reporting.html')

"""
Postings
"""
def postingshome(request):
    return render(request, 'reports/postings.html')

"""
Movements
"""


"""
Maintenance
"""
def safeworkingload(request):
    active_wire = Wire.objects.filter(status=True)
    winches = Wire.objects.all().select_related()

    context = {
        'active_wire': active_wire,
        'winches': winches,
        }

    return render(request, 'reports/safeworkingload.html', context=context)

def wireinventory(request):
    wire_inventory = Wire.objects.all()

    context = {
        'wire_inventory': wire_inventory,
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
    fields=['wireropeid','manufacturerid','nsfid','dateacquired','notes','status']
    
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

class DeploymentAdd(CreateView):
    model = DeploymentType
    template_name="wwdb/deploymentadd.html"
    fields=['name','equipment','notes','status']

"""
CUTBACKRETERMINATION
Classes related to create, update, view CutbackRetermination model
"""

class CutbackReterminationList(ListView):
    model = CutbackRetermination
    template_name="wwdb/cutbackreterminationlist.html"

class CutbackReterminationDetail(DetailView):
    model = CutbackRetermination
    template_name="wwdb/cutbackreterminationdetail.html"

class CutbackReterminationEdit(UpdateView):
    model = CutbackRetermination
    template_name="wwdb/cutbackreterminationedit.html"
    fields=['equipment','notes']

class CutbackReterminationAdd(CreateView):
    model = CutbackRetermination
    template_name="wwdb/cutbackreterminationadd.html"
    fields=['dryendtag','wetendtag', 'lengthremoved','wireid','date','notes']
    
"""
datetimepicker using admin widget
    def get_form(self, form_class=None):
        form = super(EndCast, self).get_form(form_class)
        form.fields['enddate'].widget = AdminDateWidget(attrs={'type': 'date'})
        return form

#datetimepicker using bootstrap4
    def get_form(self):
        form = super().get_form()
        form.fields['enddate'].widget = DateTimePickerInput()
        return form
"""

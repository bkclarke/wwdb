from django import template
from django.http import HttpResponse, Http404
from django.template import loader
from .models import *
from django.views.generic import *
from django.urls import reverse_lazy
from django.urls import reverse
from bootstrap_datepicker_plus.widgets import *
from .forms import *
from django.shortcuts import render 

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

class CastDetail(DetailView):
    model = Cast
    template_name="wwdb/castdetail.html"

class CastEdit(UpdateView):
    model = Cast
    template_name="wwdb/castedit.html"
    fields=['startoperatorid','endoperatorid','startdate','deploymenttypeid','winchid','notes']

class CastDelete(DeleteView):
    model = Cast
    template_name="wwdb/castdelete.html"
    success_url= reverse_lazy('home')

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
CASTS
Classes related to starting and ending a cast, viewing and updating after ending a cast, Cast model
"""

class CastStart(CreateView):
    model = Cast
    template_name="wwdb/caststart.html"
    fields=['startoperatorid','startdate','deploymenttypeid','winchid','notes']
 
#datetimepicker using bootstrap4
    def get_form(self):
        form = super().get_form()
        form.fields['startdate'].widget = DateTimePickerInput()
        return form

#datetimepicker using admin widget
#    def get_form(self, form_class=None):
#        form = super(StartCast, self).get_form(form_class)
#        form.fields['startdate'].widget = AdminDateWidget(attrs={'type': 'date'})
#        form.fields['starttime'].widget = AdminDateWidget(attrs={'type': 'time'})
#        return form

    def form_valid(self, form):
        item = form.save()
        self.pk = item.pk
        return super(CastStart, self).form_valid(form)

    def get_success_url(self):
       return reverse('castend', kwargs={'pk': self.pk})


class CastEndDetail(DetailView):
    model = Cast
    template_name="wwdb/castenddetail.html"
               
class CastEnd(UpdateView):
    model = Cast
    template_name="wwdb/castend.html"
    fields=['endoperatorid','enddate','notes']


#datetimepicker using bootstrap4
    def get_form(self):
        form = super().get_form()
        form.fields['enddate'].widget = DateTimePickerInput()
        return form

    def form_valid(self, form):
        item = form.save()
        self.pk = item.pk
        return super(CastEnd, self).form_valid(form)

    def get_success_url(self):
       return reverse('castenddetail', kwargs={'pk': self.pk})

"""
datetimepicker using admin widget
    def get_form(self, form_class=None):
        form = super(EndCast, self).get_form(form_class)
        form.fields['enddate'].widget = AdminDateWidget(attrs={'type': 'date'})
        return form
"""

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
    fields=['dryendtag','wetendtag', 'lengthremoved','wireid','date','notes','terminationid']

"""
def index(request):
    return HttpResponse("Welcome to WWDB")


def wire(request, wire_id):
    wire = Wire.objects.get(id=wire_id)
    template = loader.get_template('wwdb/wire.html')
    context = {
        'wire': wire,
    }
    return HttpResponse(template.render(context, request))

def wiretest(request, wire_id):
    wire = Wire.objects.get(id=wire_id)
    template = loader.get_template('wwdb/wiretest.html')
    context = {
        'wire': wire,
    }
    return HttpResponse(template.render(context, request))

def startcast(request):
    submitted = False
    form = startcastform
    id = Cast.objects.get(primary_key)
    if request.method == "POST":
        form = startcastform(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/wwdb/endcast')
    else:
        form = startcastform 
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'wwdb/startcast.html', {'form':form, 'submitted':submitted, 'id':id})

def endcast(request):
    submitted = False
    form = endcastform
    if request.method == "POST":
        form = endcastform(request.POST)
        if form.is_valid():
            form.update()
            return HttpResponseRedirect('/wwdb/castcomplete')
   else:
        form = endcastform 
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'wwdb/endcast.html', {'form':form, 'submitted':submitted})


def endcast(request, id):
    idlast=Cast.objects.last()
    instance = get_object_or_404(Cast, id=idlast)
    form = endcastform(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('wwdb/castcomplete')
    return render(request, 'wwdb/endcast.html', {'form': form}) 
 
def castcomplete(request):
    return HttpResponse("Cast Complete")
"""



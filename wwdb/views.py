from django import template
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from .models import Wire
from django.template import RequestContext
from django.shortcuts import render
from .models import Cast, Winchoperator
#from .forms import endcastform, startcastform
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
#from django import forms
#from django.contrib.admin.widgets import AdminTimeWidget, AdminDateWidget
from django.urls import reverse

class CastList(ListView):
    model = Cast
    template_name="wwdb/home.html"

class CastDetail(DetailView):
    model = Cast
    template_name="wwdb/castdetail.html"

class StartCast(CreateView):
    model = Cast
    template_name="wwdb/startcast.html"
    fields=['operatorid','startdate','deploymenttypeid','winchid','notes']
#    def get_form(self, form_class=None):
#        form = super(StartCast, self).get_form(form_class)
#        form.fields['startdate'].widget = AdminDateWidget(attrs={'type': 'date'})
#        return form

def endcastsuccess(request):
    template = loader.get_template('wwdb/endcastsuccess.html')
    context = {}
    return HttpResponse(template.render(context, request))
               
class EndCast(UpdateView):
    model = Cast
    template_name="wwdb/endcast.html"
    fields=['operatorid','enddate','notes']
#    def get_form(self, form_class=None):
#        form = super(StartCast, self).get_form(form_class)
#        form.fields['enddate'].widget = AdminDateWidget(attrs={'type': 'date'})
#        return form
    success_url= reverse_lazy('endcastsuccess')

class EditCast(UpdateView):
    model = Cast
    template_name="wwdb/editcast.html"
    fields=['operatorid','startdate','deploymenttypeid','winchid','notes']

class DeleteCast(DeleteView):
    model = Cast
    template_name="wwdb/deletecast.html"
    success_url= reverse_lazy('home')

class UserSettings(ListView):
    model = Winchoperator
    template_name="wwdb/usersettings.html"

class UserDetail(DetailView):
    model = Winchoperator
    template_name="wwdb/userdetail.html"

class AddUser(CreateView):
    model = Winchoperator
    template_name="wwdb/adduser.html"
    fields=['username','firstname','lastname','status']

"""
def index(request):
    return HttpResponse("Welcome to WWDB")

def wirelist(request):
    wire_list = Wire.objects.filter(status = '1').order_by('-id')[:5]
    template = loader.get_template('wwdb/wirelist.html')
    context = {
        'wire_list': wire_list,
    }
    return HttpResponse(template.render(context, request))

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



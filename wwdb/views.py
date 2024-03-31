from typing_extensions import Concatenate
from django import template
from django.db.models.query import QuerySet
from django.http import HttpResponse, Http404, HttpResponseRedirect, FileResponse
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
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch, mm
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
import io
from datetime import datetime

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
    
    castfilter = CastFilter(request.GET, queryset=cast_uricomplete)
    cast_uricomplete= castfilter.qs

    context = {
        'cast_uricomplete': cast_uricomplete,
        'cast_flag': cast_flag,
        'castfilter':castfilter,
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

    context["form", obj] = form
    return render(request, "wwdb/casts/castedit.html", context)

def castmanualenter(request):
    context ={}
    form = ManualCastForm(request.POST or None)
    if request.method == "POST":
        form = ManualCastForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            cast=Cast.objects.last()
            return HttpResponseRedirect("/wwdb/casts/%i/castenddetail" % cast.pk)
    else:
        form = ManualCastForm
        if 'submitted' in request.GET:
            submitted = True
            return render(request, 'wwdb/casts/castmanualenter.html', {'form':form, 'submitted':submitted, 'id':id})

    context['form']= form

    return render(request, "wwdb/casts/castmanualenter.html", context)

def castmanualedit(request, id):
    context ={}
    obj = Cast.objects.get(id=id)
    if request.method == 'POST':
        form = ManualCastForm(request.POST, instance = obj)
        if form.is_valid():
            form.save()
            obj.save()
            return HttpResponseRedirect('/wwdb/reports/castlist')
    else:
        form = ManualCastForm(instance = obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/wwdb/casts/%i/manualedit' % cast.pk)

    context["form"] = form
    return render(request, "wwdb/casts/castmanualedit.html", context)


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
    cutback_retermination=CutbackRetermination.objects.filter(wire=pk)
    break_test=Breaktest.objects.filter(wire=pk)

    context ={
        'wire':wire,
        'wire_object':wire_object,
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

def is_valid_queryparam(param):
    return param != '' and param is not None

def unols_form_filter(request):
    
    qs = Cast.objects.all()
    wire = request.GET.get('wire_nsfid')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')

    if is_valid_queryparam(date_min):
        qs=qs.filter(startdate__gte=date_min)

    if is_valid_queryparam(date_max):
        qs=qs.filter(enddate__lt=date_max)

    return qs

def unolswirereport(request):
    wire=Wire.objects.all()
    qs = unols_form_filter(request)

    context = {
        'qs':qs,
        'wire':wire,
        }

    return render(request, "wwdb/reports/unolswirereport.html", context)

def unols_wire_report_file(request):
    cast = unols_form_filter(request)

    response = HttpResponse(content_type="text/plain")
    response['Content-Disposition']='attachement; filename=cruise_reports.txt'

    #create dictionary of active winch keys and cast object list values
    cast_by_winch = {}
    for c in cast:
        if c.active_winch not in cast_by_winch:
            cast_by_winch[c.active_winch] = []

        cast_by_winch[c.active_winch].append(c)
        
    #create dictionary of active winch keys and integer value of casts completed values
    cast_by_winch_count = {}
    for c in cast_by_winch:
        cast_by_winch_count[c]=len(cast_by_winch[c])

    #create dictionary of active winch keys and maxtension list values of casts completed
    tension_by_winch = {}
    for c in cast:
        if c.active_winch not in tension_by_winch:
            tension_by_winch[c.active_winch] = []
        tension_by_winch[c.active_winch].append(c.maxtension)

    # filter none values from key value lists
    for t in tension_by_winch:
        tension_by_winch[t]=list(filter(lambda item: item is not None,tension_by_winch[t]))

    #Create dictionary of active winch keys and max tension per winch values
    maxtension_by_winch={}
    for t in tension_by_winch:
        if tension_by_winch[t]:
            maxtension_by_winch[t]=max(tension_by_winch[t])
        else:
            maxtension_by_winch[t]='None'

    #create dictionary of active winch keys and max payout list values of casts completed
    payout_by_winch = {}
    for c in cast:
        if c.active_winch not in payout_by_winch:
            payout_by_winch[c.active_winch] = []
        payout_by_winch[c.active_winch].append(c.maxpayout)

    #Create dictionary of active winch keys and max payout per winch values
    for t in payout_by_winch:
        payout_by_winch[t]=list(filter(lambda item: item is not None,payout_by_winch[t]))

    #Create dictionary of active winch keys and max payout per winch values
    maxpayout_by_winch={}
    for t in payout_by_winch:
        if payout_by_winch[t]:
            maxpayout_by_winch[t]=max(payout_by_winch[t])
        else:
            maxpayout_by_winch[t]='None'

    #append data to list, write to file
    lines = []

    lines.append('\n#Start date:' + str(date_min))
    lines.append('\n#End Date:' + str(date_max))

    lines.append('\n#\n#')

    for t in maxtension_by_winch:
        lines.append('\n#' + str(t) + ' Max tension: ' + str(maxtension_by_winch[t]))

    lines.append('\n#\n#')

    for t in maxpayout_by_winch:
        lines.append('\n#' + str(t) + ' Max payout: ' + str(maxpayout_by_winch[t]))

    lines.append('\n#\nstarttime, endtime, winch, deploymenttype, startoperator, endoperator, maxtension, maxpayout, payoutmaxtension, metermaxtension, timemaxtension, wetendtag, dryendtag, notes')

    for c in cast:
            lines.append('\n' + str(c.startdate) + ',' 
            +  str(c.enddate) + ',' 
            +  str(c.active_winch) + ',' 
            +  str(c.deploymenttype) + ',' 
            +  str(c.startoperator) + ',' 
            +  str(c.endoperator) + ',' 
            +  str(c.maxtension) + ',' 
            +  str(c.maxpayout) + ',' 
            +  str(c.payoutmaxtension) + ',' 
            +  str(c.metermaxtension) + ',' 
            +  str(c.timemaxtension) + ','
            +  str(c.wetendtag) + ',' 
            +  str(c.dryendtag) + ',' 
            +  str(c.notes) + ',' )


    response.writelines(lines)


    return response

def cruisereport(request, pk):
    
    #cruise object and casts by cruise daterange
    cruise=Cruise.objects.filter(id=pk)
    cruise_object=cruise.last()
    startdate=cruise_object.startdate
    enddate=cruise_object.enddate
    cast = Cast.objects.filter(startdate__range=[startdate, enddate])

    #create dictionary of active winch keys and cast object list values
    cast_by_winch = {}
    for c in cast:
        if c.active_winch not in cast_by_winch:
            cast_by_winch[c.active_winch] = []

        cast_by_winch[c.active_winch].append(c)
        
    #create dictionary of active winch keys and integer value of casts completed values
    cast_by_winch_count = {}
    for c in cast_by_winch:
        cast_by_winch_count[c]=len(cast_by_winch[c])

    #create dictionary of active winch keys and maxtension list values of casts completed
    tension_by_winch = {}
    for c in cast:
        if c.active_winch not in tension_by_winch:
            tension_by_winch[c.active_winch] = []
        tension_by_winch[c.active_winch].append(c.maxtension)

    # filter none values from key value lists
    for t in tension_by_winch:
        tension_by_winch[t]=list(filter(lambda item: item is not None,tension_by_winch[t]))

    #Create dictionary of active winch keys and max tension per winch values
    maxtension_by_winch={}
    for t in tension_by_winch:
        if tension_by_winch[t]:
            maxtension_by_winch[t]=max(tension_by_winch[t])
        else:
            maxtension_by_winch[t]='None'

    #create dictionary of active winch keys and max payout list values of casts completed
    payout_by_winch = {}
    for c in cast:
        if c.active_winch not in payout_by_winch:
            payout_by_winch[c.active_winch] = []
        payout_by_winch[c.active_winch].append(c.maxpayout)

    #Create dictionary of active winch keys and max payout per winch values
    for t in payout_by_winch:
        payout_by_winch[t]=list(filter(lambda item: item is not None,payout_by_winch[t]))

    #Create dictionary of active winch keys and max payout per winch values
    maxpayout_by_winch={}
    for t in payout_by_winch:
        if payout_by_winch[t]:
            maxpayout_by_winch[t]=max(payout_by_winch[t])
        else:
            maxpayout_by_winch[t]='None'

    context = {
        "cruise": cruise,
        "cast": cast,
        "cast_by_winch_count": cast_by_winch_count,
        "maxtension_by_winch":maxtension_by_winch,
        "maxpayout_by_winch":maxpayout_by_winch,
    }

    return render(request, "wwdb/reports/cruisereport.html", context)

def cruise_report_file(request, pk):

    #cruise object and casts by cruise daterange
    cruise=Cruise.objects.filter(id=pk)
    cruise_object=cruise.last()
    startdate=cruise_object.startdate
    enddate=cruise_object.enddate
    cast = Cast.objects.filter(startdate__range=[startdate, enddate])
    cruisenumber=cruise_object.number

    response = HttpResponse(content_type="text/plain")
    response['Content-Disposition']='attachement; filename=cruise_report_' + str(cruisenumber) + '.txt'

    #cruise object and casts by cruise daterange
    cruise=Cruise.objects.filter(id=pk)
    cruise_object=cruise.last()
    startdate=cruise_object.startdate
    enddate=cruise_object.enddate
    cast = Cast.objects.filter(startdate__range=[startdate, enddate])

    #create dictionary of active winch keys and cast object list values
    cast_by_winch = {}
    for c in cast:
        if c.active_winch not in cast_by_winch:
            cast_by_winch[c.active_winch] = []

        cast_by_winch[c.active_winch].append(c)
        
    #create dictionary of active winch keys and integer value of casts completed values
    cast_by_winch_count = {}
    for c in cast_by_winch:
        cast_by_winch_count[c]=len(cast_by_winch[c])

    #create dictionary of active winch keys and maxtension list values of casts completed
    tension_by_winch = {}
    for c in cast:
        if c.active_winch not in tension_by_winch:
            tension_by_winch[c.active_winch] = []
        tension_by_winch[c.active_winch].append(c.maxtension)

    # filter none values from key value lists
    for t in tension_by_winch:
        tension_by_winch[t]=list(filter(lambda item: item is not None,tension_by_winch[t]))

    #Create dictionary of active winch keys and max tension per winch values
    maxtension_by_winch={}
    for t in tension_by_winch:
        if tension_by_winch[t]:
            maxtension_by_winch[t]=max(tension_by_winch[t])
        else:
            maxtension_by_winch[t]='None'

    #create dictionary of active winch keys and max payout list values of casts completed
    payout_by_winch = {}
    for c in cast:
        if c.active_winch not in payout_by_winch:
            payout_by_winch[c.active_winch] = []
        payout_by_winch[c.active_winch].append(c.maxpayout)

    #Create dictionary of active winch keys and max payout per winch values
    for t in payout_by_winch:
        payout_by_winch[t]=list(filter(lambda item: item is not None,payout_by_winch[t]))

    #Create dictionary of active winch keys and max payout per winch values
    maxpayout_by_winch={}
    for t in payout_by_winch:
        if payout_by_winch[t]:
            maxpayout_by_winch[t]=max(payout_by_winch[t])
        else:
            maxpayout_by_winch[t]='None'

    #append data to list, write to file
    lines = []
    lines.append('#' + cruise_object.number)

    lines.append('\n#Start date:' + str(startdate))
    lines.append('\n#End Date:' + str(enddate))

    lines.append('\n#\n#')

    for t in maxtension_by_winch:
        lines.append('\n#' + str(t) + ' Max tension: ' + str(maxtension_by_winch[t]))

    lines.append('\n#\n#')

    for t in maxpayout_by_winch:
        lines.append('\n#' + str(t) + ' Max payout: ' + str(maxpayout_by_winch[t]))

    lines.append('\n#\nstarttime, endtime, winch, deploymenttype, startoperator, endoperator, maxtension, maxpayout, payoutmaxtension, metermaxtension, timemaxtension, wetendtag, dryendtag, notes')

    for c in cast:
            lines.append('\n' + str(c.startdate) + ',' 
            +  str(c.enddate) + ',' 
            +  str(c.active_winch) + ',' 
            +  str(c.deploymenttype) + ',' 
            +  str(c.startoperator) + ',' 
            +  str(c.endoperator) + ',' 
            +  str(c.maxtension) + ',' 
            +  str(c.maxpayout) + ',' 
            +  str(c.payoutmaxtension) + ',' 
            +  str(c.metermaxtension) + ',' 
            +  str(c.timemaxtension) + ','
            +  str(c.wetendtag) + ',' 
            +  str(c.dryendtag) + ',' 
            +  str(c.notes) + ',' )


    response.writelines(lines)

    return response

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

def safeworkingtensions_file(request):

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer)

    #Set canvas as landscape A4
    c.setPageSize(landscape(A4))

    #Draw title
    c.setFont("Helvetica", 36, leading=None)
    c.drawString(1*inch,7*inch,"Safe Working Tensions")

    #Create formatted datetime object 
    now=datetime.now()
    date_time=now.strftime('%m/%d/%Y')
    date_time_filename=now.strftime('%Y%m%d')

    #draw date posted on canvas
    c.setFont("Helvetica", 12, leading=None)
    c.drawString(1*inch,1*inch,"date posted: " + date_time)

    #create empty lines list object
    lines = []
    
    #wire objects where status=True, ordered by winch name in ascending order
    active_wire = Wire.objects.filter(status=True).order_by('-winch')
    
    #Define stylesheet for headers
    stylesheet=getSampleStyleSheet()
    HeaderStyle=ParagraphStyle('yourtitle',
                           fontName="Helvetica-Bold",
                           fontSize=16,
                           parent=stylesheet['Heading2'],
                           alignment=TA_LEFT,
                           spaceAfter=14)

    #Define header objects
    header1=Paragraph('winch',HeaderStyle)
    header2=Paragraph('Wire ID',HeaderStyle)
    header3=Paragraph('Length',HeaderStyle)
    header4=Paragraph('Factor of Safety',HeaderStyle)
    header5=Paragraph('Safe Working Tension',HeaderStyle)

    #append headers to lines list
    lines.append((header1,header2,header3,header4,header5))
    
    #append wire data to lines list
    for wire in active_wire:
        lines.append((wire.winch.name, 
                      wire.nsfid, 
                      wire.active_length, 
                      wire.factorofsafety, 
                      wire.safe_working_tension))
    
    #Define table settings and styles, add lines list to table
    table = Table(lines,
                  colWidths=[100,175,100,155,155],
                  rowHeights=[100,100,100,100])

    table.setStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ('LINEABOVE', (0, 1), (-1, -1), 0.10, colors.grey),
                    ('FONTSIZE',(0,0),(-1,-1),24)])
    
    width, height = A4
    table.wrapOn(c, width, height)

    #Draw table on canvas
    table.drawOn(c, 1 * inch, 1.5 * inch)

    c.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='safe_working_tension_%s.pdf' %date_time_filename)

"""
Maintenance
"""

def wirelist(request):
    wires_in_use = Wire.objects.filter(status=True)
    wires_in_storage = Wire.objects.filter(status=False)
    wires = Wire.objects.all()
    
    context = {
        'wires_in_use': wires_in_use,
        'wires_in_storage': wires_in_storage, 
        'wires' : wires,
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
            obj.edit_length()
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
            obj.submit_length()
            obj.submit_dry_end_tag()
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


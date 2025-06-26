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
from datetime import datetime, timedelta, timezone
from django.db.models import Q
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.contrib.auth import logout
from django.core.exceptions import ValidationError
from math import ceil
from dateutil import parser
import traceback
from django.db import transaction



logger = logging.getLogger(__name__)



def _parse_iso(ts: str) -> datetime:
    return parser.isoparse(ts)

def chart_data_zoom(request):
    """AJAX endpoint that returns rebinned data for the visible range."""
    try:
        start = _parse_iso(request.GET["start"])
        end = _parse_iso(request.GET["end"])
        print(request.GET.get("winch"))
        winch_id = request.GET.get("winch", "").strip()
        max_points = min(int(request.GET.get("max_points", MAX_POINTS)), MAX_CAP)

        if not winch_id.isdigit():
            raise ValueError("Invalid winch ID")

        winch = Winch.objects.get(id=int(winch_id))
        data_pts = get_data_from_external_db(start, end, winch.name)
        data_pts = auto_bin_to_target(data_pts, max_points=max_points)

        data_t = [
            {"date": dt.strftime("%Y-%m-%d %H:%M:%S"), "value": v["max_tension"]}
            for dt, v in data_pts
        ]
        data_p = [
            {"date": dt.strftime("%Y-%m-%d %H:%M:%S"), "value": v["max_payout"]}
            for dt, v in data_pts
        ]
        return JsonResponse({"tension": data_t, "payout": data_p})

    except Exception as e:
        traceback.print_exc()
        print("chart_data_zoom ERROR:", e)
        return JsonResponse({"error": str(e)}, status=400)

def bin_data(data_points, *, bin_minutes: float) -> list:

    if not data_points:
        return []

    bin_delta = timedelta(minutes=bin_minutes)
    binned    = []

    bin_start   = data_points[0][0]
    bin_end     = bin_start + bin_delta
    bin_tens    = []
    bin_payouts = []

    for dt, vals in data_points:
        while dt >= bin_end:                        # time to close the bin
            if bin_tens:                           # avoid /0
                avg_t = sum(t for t in bin_tens    if t is not None) / len(bin_tens)
                avg_p = sum(p for p in bin_payouts if p is not None) / len(bin_payouts)
            else:
                avg_t = avg_p = None

            binned.append((bin_start, {'max_tension': avg_t, 'max_payout': avg_p}))
            bin_start   = bin_end
            bin_end     = bin_start + bin_delta
            bin_tens    = []
            bin_payouts = []

        bin_tens.append(vals['max_tension'])
        bin_payouts.append(vals['max_payout'])

    # final partially filled bin
    if bin_tens:
        avg_t = sum(t for t in bin_tens    if t is not None) / len(bin_tens)
        avg_p = sum(p for p in bin_payouts if p is not None) / len(bin_payouts)
        binned.append((bin_start, {'max_tension': avg_t, 'max_payout': avg_p}))

    return binned

MAX_DAYS = 14
MAX_PROCESS_SECONDS = 5  
MAX_POINTS  = 2000  
MAX_CAP = 5000 
MIN_BIN_SEC = 1 

def auto_bin_to_target(data_points, max_points=MAX_POINTS):

    n = len(data_points)
    if n <= max_points:
        return data_points                        # already small

    # overall timespan in seconds
    total_sec = (data_points[-1][0] - data_points[0][0]).total_seconds()
    if total_sec <= 0:
        return data_points[:max_points]           # degenerate, just clip

    bin_sec = max(MIN_BIN_SEC, ceil(total_sec / max_points))
    bin_minutes = bin_sec / 60.0

    binned = bin_data(data_points, bin_minutes=bin_minutes)

    if len(binned) > max_points:
        step = ceil(len(binned) / max_points)
        binned = binned[::step]

    return binned

def get_data_from_external_db(start_date, end_date, winch):
    try:
        conn_str = 'Driver={SQL Server};Server=EN-WINCH\MSSQLSERVER01, 1433;Database=WinchDb;Trusted_Connection=no;UID=remoteadmin;PWD=eris.2003;'

        start_str = start_date.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        end_str   = end_date.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


        query = f"""
            SELECT DateTime, Tension, Payout
            FROM {winch}
            WHERE DateTime BETWEEN '{start_str}' AND '{end_str}'
            """

        with pyodbc.connect(conn_str) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return [(row[0], {'max_tension': row[1], 'max_payout': row[2]}) for row in rows]

    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def charts(request):
    db_connected = True
    error_message = None

    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    winch_id = request.GET.get("winch") or '3'
    if not winch_id:
        winch = Winch.objects.last()     # fallback to any winch you like
    else:
        winch = Winch.objects.get(id=int(winch_id))

    # Validate input and limit date range
    try:
        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

            if (end_date - start_date).days > MAX_DAYS:
                error_message = f"Please select a date range of {MAX_DAYS} days or less."

            # Include full day
            end_date = end_date + timedelta(days=1)
        else:
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=1)
            end_date = end_date + timedelta(days=1)

    except ValueError:
        error_message = "Invalid date format."



    try:
        winch = Winch.objects.get(id=int(winch_id))
    except (Winch.DoesNotExist, ValueError):
        winch = Winch.objects.last()

    data_tension = []
    data_payout = []

    if not error_message:
        data_points = get_data_from_external_db(start_date, end_date, winch.name)

        if data_points == 'timeout':
            error_message = "Data processing timed out. Please select a smaller date range."
            db_connected = False
            data_points = []
        elif data_points is None:
            db_connected = False
            data_points = []

        data_points = auto_bin_to_target(data_points, MAX_POINTS)

        for dt, vals in data_points:
            data_tension.append({'date': dt.strftime('%Y-%m-%d %H:%M:%S'), 'value': vals['max_tension']})
            data_payout.append({'date': dt.strftime('%Y-%m-%d %H:%M:%S'), 'value': vals['max_payout']})

    data_json_tension = json.dumps(data_tension)
    data_json_payout = json.dumps(data_payout)

    form = DataFilterForm(initial={
        'start_date': start_date.date() if start_date else None,
        'end_date': (end_date - timedelta(days=1)).date() if end_date else None,
        'winch': winch.id 
    })

    context = {
        'form': form,
        'data_json_tension': data_json_tension,
        'data_json_payout': data_json_payout,
        'db_connected': db_connected,
        'no_db_connection': not db_connected,
    }

    return render(request, 'wwdb/reports/charts.html', context)

def custom_logout(request):
    logout(request)  # Logs out the user
    return redirect('home')  # Redirects to the homepage

def home(request):
    template_name = 'home.html'
    context = {
        'template_name': template_name,
        }

    return render(request, "wwdb/home.html", context)

'''
Test reactive HTMX tables
'''
"""
def operatortablelistget(request):
    context = {}
    context['winchoperator'] = WinchOperator.objects.all()
    return render(request, 'wwdb/operatortablelist.html', context)

def operatortable(request):
    context = {'form': WinchOperatorTableForm()}
    return render(request, 'wwdb/add_winchoperator.html', context)

def add_winchoperator_submit(request):
    context = {}
    form = WinchOperatorTableForm(request.POST)
    context['form'] = form
    if form.is_valid():
        context['winchoperator'] = form.save()
    else:
        return render(request, 'wwdb/add_winchoperator.html', context)
    return render(request, 'wwdb/winchoperator_row.html', context)

def add_winchoperator_cancel(request):
    return HttpResponse()

def delete_winchoperator(request, winchoperator_pk):
    winchoperator = WinchOperator.objects.get(pk=winchoperator_pk)
    winchoperator.delete()
    return HttpResponse()

def edit_winchoperator(request, winchoperator_pk):
    winchoperator = WinchOperator.objects.get(pk=winchoperator_pk)
    context = {}
    context['winchoperator'] = winchoperator
    context['form'] = WinchOperatorTableForm(initial={
        'firstname':winchoperator.firstname,
        'lastname': winchoperator.lastname,
        'status': winchoperator.status,
        'username': winchoperator.username,
    })
    return render(request, 'wwdb/edit_winchoperator.html', context)

def edit_winchoperator_submit(request, winchoperator_pk):
    context = {}
    winchoperator = WinchOperator.objects.get(pk=winchoperator_pk)
    context['winchoperator'] = winchoperator
    if request.method == 'POST':
        form = WinchOperatorForm(request.POST, instance=winchoperator)
        if form.is_valid():
            form.save()
        else:
            return render(request, 'wwdb/edit_winchoperator.html', context)
    return render(request, 'wwdb/winchoperator_row.html', context)

def home(request):
    template = loader.get_template('wwdb/home.html')
    context = {}
    return HttpResponse(template.render(context, request))
"""
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
            cast=Cast.objects.last()
            cast.refresh_from_db()
            if cast.startdate == None:
                cast.startcast_get_datetime()
            cast.save()
            return HttpResponseRedirect("%i/castend" % cast.pk)
    else:
        form = StartCastForm 
        if 'submitted' in request.GET:
            submitted = True
            return render(request, 'wwdb/casts/caststart.html', {'form':form, 'submitted':submitted, 'id':id})

    template_name = 'caststart.html'

    context = {
        'form':form,
        'template_name':template_name}
    return render(request, "wwdb/casts/caststart.html", context)

def caststartend(request):
    form = StartEndCastForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            cast = form.save()
            cast.refresh_from_db()
            cast.get_active_wire()
            cast.endcastcal()
            cast.get_active_length()
            cast.get_active_safeworkingtension()
            cast.get_active_factorofsafety()
            cast.save()
            cast.refresh_from_db()
            cast.get_cast_duration()
            cast.save()
            return HttpResponseRedirect('/wwdb/reports/castreport')
        else:
            print(form.errors)

    # Add this line to handle GET or invalid POST
    return render(request, 'wwdb/casts/caststartend.html', {'form': form})


def castlist(request):
    casts = Cast.objects.filter(deleted=False).order_by('-starttime')  # Or however you're fetching them

    context = {
        'casts': casts,
       }

    return render(request, 'wwdb/reports/castlist.html', context=context)

def cast_end(request):
    last = Cast.objects.latest('pk')
    return redirect('castend', id=last.pk)
	
def castend(request, id):
    context ={}
    obj = Cast.objects.get(id=id)
    form = EndCastForm(request.POST or None, instance = obj)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            if obj.enddate == None:
                obj.endcast_get_datetime()
            obj.save()
            obj.refresh_from_db()
            obj.get_active_wire()
            obj.endcastcal()
            obj.get_cast_duration()
            obj.save()

            return HttpResponseRedirect("/wwdb/casts/%i/castenddetail" % obj.pk)
    context["form"] = form

    template_name = 'castend.html'

    context = {
        'form':form,
        'template_name':template_name}

    return render(request, "wwdb/casts/castend.html", context)

def updateallcasts(request):
    if request.method == 'POST':
        casts = Cast.objects.all()
        updated_count = 0

        for cast in casts:
            winch=cast.winch.name
            if winch=='winch1' or winch=='winch2' or winch=='winch3':
                if cast.enddate and cast.startdate:
                    print(cast)
                    start = cast.startdate
                    end = cast.enddate   
                    duration = (end - start)          
                    duration_in_minutes = round(duration.total_seconds() / 60)
                    cast.duration = duration_in_minutes
                    print(cast.duration)
                    cast.save()
                    updated_count += 1
                    print(updated_count)


        # You could use messages to notify about the result
        # from django.contrib import messages
        # messages.success(request, f'Successfully updated {updated_count} casts.')

        return redirect('/wwdb/reports/castreport')  # Or another page

    return render(request, 'wwdb/casts/updateallcasts.html')

def castedit(request, id):
    context ={}
        
    obj = Cast.objects.get(id=id)
    if request.method == 'POST':
        form = EditCastForm(request.POST, instance = obj)
        if form.is_valid():
            form.save()
            obj.get_active_wire()
            obj.endcastcal()
            obj.save()

            obj.refresh_from_db()
            obj.get_cast_duration()
            obj.save()

            return HttpResponseRedirect('/wwdb/reports/castreport')
    else:
        form = EditCastForm(instance = obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/wwdb/casts/%i/edit' % obj.pk)

    context["form"] = form
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
            return HttpResponseRedirect('/wwdb/reports/castreport')
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
    success_url= reverse_lazy('castreport')

def castenddetail(request, id):
    context ={}
    context["cast"] = Cast.objects.get(id = id)
    return render(request, "wwdb/casts/castenddetail.html", context)

"""
PRECRUISE CONFIGURATION
Classes related to starting a cruise including updating WinchOperators and DeploymentType models
"""

def castconfigurehome(request):
    operators = WinchOperator.objects.all()
    deployments = DeploymentType.objects.all()
    active_wire = Wire.objects.filter(status=True)
    winches = Winch.objects.all()
    cruises = Cruise.objects.all()

    context = {
        'operators': operators,
        'deployments': deployments,
        'active_wire': active_wire,
        'winches': winches,
        'cruises' : cruises,
       }

    return render(request, 'wwdb/configuration/castconfiguration.html', context=context)

def cruiseconfigurehome(request):
    cruises = Cruise.objects.all()

    context = {
        'cruises' : cruises,
       }

    return render(request, 'wwdb/configuration/cruiseconfiguration.html', context=context)


class CruiseDelete(DeleteView):
    model = Cruise
    template_name="wwdb/cruiseconfiguration/cruisedelete.html"
    success_url= reverse_lazy('cruiseconfigurehome')

def wireeditfactorofsafety(request, id):
    context ={}
    obj = get_object_or_404(Wire, id = id)

    if request.method == 'POST':
        form = EditFactorofSafetyForm(request.POST, instance = obj)
        if form.is_valid():
            form.save()
            wireid=Wire.objects.get(id=id)
            return HttpResponseRedirect("/wwdb/configuration/castconfiguration")
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

def castreport(request):
    # Initialize form with data from GET request (if any)
    form = CastFilterForm(request.GET)
    casts = Cast.objects.all().order_by('-startdate')

    # Handle form submission and filtering
    if form.is_valid():
        casts = Cast.objects.all()
        deploymenttype = form.cleaned_data.get('deploymenttype')
        winch = form.cleaned_data.get('winch')
        startdate = form.cleaned_data.get('startdate')
        enddate = form.cleaned_data.get('enddate')
        wire = form.cleaned_data.get('wire')
        operator = form.cleaned_data.get('operator')
        if deploymenttype:
            casts = casts.filter(deploymenttype=deploymenttype)
        if winch:
            casts = casts.filter(winch=winch)
        if startdate:    
            casts = casts.filter(startdate__gte=startdate)
        if enddate:
            casts = casts.filter(enddate__lte=enddate)
        if wire:
            casts = casts.filter(wire=wire)
        if operator:
            casts = casts.filter(Q(startoperator=operator) | Q(endoperator=operator))

    context = {
        'casts': casts,
        'form': form,
       }
    # Render the template with form and filtered products
    return render(request, 'wwdb/reports/castreport.html', context)

"""
def is_valid_queryparam(param):
    return param != '' and param is not None


def cast_table_filter(request):
    
    qs = Cast.objects.all()
    wire = request.GET.get('wire_nsfid')
    winch = request.GET.get('winch_id')
    deployment = request.GET.get('deployment_id')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')

    if is_valid_queryparam(date_min):
        qs=qs.filter(startdate__gte=date_min)

    if is_valid_queryparam(date_max):
        qs=qs.filter(enddate__lt=date_max)

    if is_valid_queryparam(wire):
        if wire!='Wire':
            wire_obj=Wire.objects.filter(nsfid=wire).last()
            qs=qs.filter(wire=wire_obj)

    if is_valid_queryparam(winch):
        if winch!='Winch':
            winch_obj=Winch.objects.filter(name=winch).last()
            qs=qs.filter(winch=winch_obj)

    if is_valid_queryparam(deployment):
        if deployment!='Deployment':
            deployment_obj=DeploymentType.objects.filter(name=deployment).last()
            qs=qs.filter(deploymenttype=deployment_obj)

    return qs

def castreport(request):
    wire=Wire.objects.all()
    winch=Winch.objects.all()
    deployment=DeploymentType.objects.all()
    qs = cast_table_filter(request)



    context = {
        'qs':qs,
        'wire':wire,
        'winch':winch,
        'deployment':deployment,
        }

    return render(request, "wwdb/reports/castreport.html", context)
"""

def cast_table_csv(request):
    cast = cast_table_filter(request)

    response = HttpResponse(content_type="text/plain")
    response['Content-Disposition']='attachement; filename=cast_table.csv'
    
    lines = []

    date_min=cast.order_by('startdate').first()
    date_max=cast.order_by('enddate').last()

    lines.append('\n#Start date:' + str(date_min))
    lines.append('\n#End Date:' + str(date_max))
    lines.append('\n#\n#')
    lines.append('\n#\nstarttime, endtime, winch, wire, deploymenttype, startoperator, endoperator, maxtension, maxpayout, payoutmaxtension, metermaxtension, timemaxtension, wetendtag, dryendtag, notes')

    for c in cast:
            lines.append('\n' + str(c.startdate) + ',' 
            +  str(c.enddate) + ',' 
            +  str(c.active_winch) + ',' 
            +  str(c.wire) + ','
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

def unols_report_csv(request):
    cast = cast_table_filter(request)

    response = HttpResponse(content_type="text/plain")
    response['Content-Disposition']='attachement; filename=cruise_reports.csv'

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

    #find startdatetime and enddatetime
    date_min=cast.order_by('startdate').first()
    date_max=cast.order_by('enddate').last()

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

    lines.append('\n#\nstarttime, endtime, winch, wire, deploymenttype, startoperator, endoperator, maxtension, maxpayout, payoutmaxtension, metermaxtension, timemaxtension, wetendtag, dryendtag, notes')

    for c in cast:
            lines.append('\n' + str(c.startdate) + ',' 
            +  str(c.enddate) + ',' 
            +  str(c.active_winch) + ',' 
            +  str(c.wire) + ',' 
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


def cruisereportedit(request, pk):
    obj = get_object_or_404(Cruise, id = pk)

    #cruise object and casts by cruise daterange
    cruise_object=obj
    startdate=cruise_object.startdate
    enddate=cruise_object.enddate
    casts=Cast.objects.filter(startdate__range=[startdate, enddate])
    winches=Cast.objects.filter(startdate__range=[startdate, enddate]).values('winch').distinct()

    active_winches=[]

    for w in winches:
        active_winches.append(w)

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
    cast=Cast.objects.filter(startdate__range=[startdate, enddate])

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

    #list of used winches
    active_winches=[]
    for c in cast:
        if c.active_winch not in active_winches:
            active_winches.append(c.active_winch)

    context = {
        "cruise": cruise,
        "cast": cast,
        "cast_by_winch_count": cast_by_winch_count,
        "maxtension_by_winch":maxtension_by_winch,
        "maxpayout_by_winch":maxpayout_by_winch,
        "active_winches":active_winches,
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

    response = HttpResponse(content_type="csv")
    response['Content-Disposition']='attachement; filename=wire_report_' + str(cruisenumber) + '.csv'

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

    #list of used winches
    active_winches=[]
    for c in cast:
        if c.active_winch not in active_winches:
            active_winches.append(c.active_winch)

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

    for winch in active_winches:
        if winch == 'winch1':
            lines.append('\n#\n#\n#Winch 1')
            lines.append('\n#block arrangement: ' + str(cruise_object.winch1blockarrangement))
            lines.append('\n#termination: ' + str(cruise_object.winch1termination))
            lines.append('\n#notes: ' + str(cruise_object.winch1notes))
        elif winch == 'winch2':
            lines.append('\n#\n#\n#Winch 2')
            lines.append('\n#block arrangement: ' + str(cruise_object.winch2blockarrangement))
            lines.append('\n#termination: ' + str(cruise_object.winch2termination))
            lines.append('\n#spin direction: ' + str(cruise_object.winch2spindirection))
            lines.append('\n#notes: ' + str(cruise_object.winch2notes))
        elif winch == 'winch3':
            lines.append('\n#\n#\n#Winch 3')
            lines.append('\n#block arrangement: ' + str(cruise_object.winch3blockarrangement))
            lines.append('\n#termination: ' + str(cruise_object.winch3termination))
            lines.append('\n#notes: ' + str(cruise_object.winch3notes))
        else:
            lines.append('\n#\n#\n#Science provided winch notes')
            lines.append('\n#' + str(cruise_object.scienceprovidedwinch))

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
WIRES
Classes related to create, update, view Wire model
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

def wireropedatalist(request):
    wireropes = WireRopeData.objects.all()
    
    context = {
        'wireropes': wireropes,
        }

    return render(request, 'wwdb/inventories/wireropedatalist.html', context=context)

def wireropedataedit(request, id):
    context ={}
    obj = get_object_or_404(WireRopeData, id = id)

    if request.method == 'POST':
        form = WireRopeDataEditForm(request.POST, instance = obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/wwdb/inventories/wireropedatalist")
    else:
        form = WireRopeDataEditForm(instance = obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/wwdb/inventories/wireropedata/%i/edit" % obj.pk)

    context["form"] = form
    return render(request, "wwdb/inventories/wireropedataedit.html", context)

def wireropedataadd(request):
    context ={}
    form = WireRopeDataAddForm(request.POST or None)
    if request.method == "POST":
        form = WireRopeDataAddForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/wwdb/inventories/wireropedatalist')
    else:
        form = WireRopeDataAddForm 
        if 'submitted' in request.GET:
            submitted = True
            return render(request, 'wwdb/inventories/wireropedataadd.html', {'form':form, 'submitted':submitted, 'id':id})
 
    context['form']= form

    return render(request, "wwdb/inventories/wireropedataadd.html", context)

def wireropedatadelete(request, id):
    wireropedata = WireRopeData.objects.get(pk=id)
    wireropedata.delete()
    return HttpResponse()

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
def swttablelistget(request):
    context = {}
    context['wire'] = Wire.objects.filter(status=True)
    return render(request, 'wwdb/configuration/swttablelist.html', context)

def swttableadd(request):
    context = {'form': SWTTableForm()}
    return render(request, 'wwdb/configuration/swttableadd.html', context)

def swttableaddsubmit(request):
    context = {}
    form = SWTTableForm(request.POST)
    context['form'] = form
    if form.is_valid():
        context['wire'] = form.save()
    else:
        return render(request, 'wwdb/configuration/swttableadd.html', context)
    return render(request, 'wwdb/configuration/swttablerow.html', context)

def swttableaddcancel(request):
    return HttpResponse()

def swttabledelete(request, wire_pk):
    wire = Wire.objects.get(pk=wire_pk)
    wire.delete()
    return HttpResponse()

def swttableedit(request, wire_pk):
    wire = Wire.objects.get(pk=wire_pk)
    context = {}
    context['wire'] = wire
    context['form'] = SWTTableForm(initial={
        'winch':wire.winch,
        'factorofsafety': wire.factorofsafety,
    })
    return render(request, 'wwdb/configuration/swttableedit.html', context)

def swttableeditsubmit(request, wire_pk):
    wire = Wire.objects.get(pk=wire_pk)
    context = {}
    context['wire'] = wire
    if request.method == 'POST':
        form = SWTTableForm(request.POST, instance=wire)
        if form.is_valid():
            form.save()
        else:
            return render(request, 'wwdb/configuration/swttableedit.html', context)
    return render(request, 'wwdb/configuration/swttablerow.html', context)

def winchtablelistget(request):
    context = {}
    context['winch'] = Winch.objects.all()
    return render(request, 'wwdb/configuration/winchtablelist.html', context)

def winchtableadd(request):
    context = {'form': WinchTableForm()}
    return render(request, 'wwdb/configuration/winchtableadd.html', context)

def winchtableaddsubmit(request):
    context = {}
    form = WinchTableForm(request.POST)
    context['form'] = form
    if form.is_valid():
        context['winch'] = form.save()
    else:
        return render(request, 'wwdb/configuration/winchtableadd.html', context)
    return render(request, 'wwdb/configuration/winchtablerow.html', context)

def winchtableaddcancel(request):
    return HttpResponse()

def winchtabledelete(request, winch_pk):
    winch = Winch.objects.get(pk=winch_pk)
    winch.delete()
    return HttpResponse()

def winchtableedit(request, winch_pk):
    winch = Winch.objects.get(pk=winch_pk)
    context = {}
    context['winch'] = winch
    context['form'] = WinchTableForm(initial={
        'name':winch.name,
        'status': winch.status,
    })
    return render(request, 'wwdb/configuration/winchtableedit.html', context)

def winchtableeditsubmit(request, winch_pk):
    context = {}
    winch= Winch.objects.get(pk=winch_pk)
    context['winch'] = winch
    if request.method == 'POST':
        form = WinchTableForm(request.POST, instance=winch)
        if form.is_valid():
            form.save()
        else:
            return render(request, 'wwdb/configuration/winchtablerow.html', context)
    return render(request, 'wwdb/configuration/winchtablerow.html', context)

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
            return HttpResponseRedirect("/wwdb/configuration/castconfiguration")
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
            return HttpResponseRedirect('/wwdb/configuration/castconfiguration')
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

def operatortablelistget(request):
    context = {}
    context['winchoperator'] = WinchOperator.objects.all()
    return render(request, 'wwdb/configuration/operatortablelist.html', context)

def operatortableadd(request):
    context = {'form': WinchOperatorTableForm()}
    return render(request, 'wwdb/configuration/operatortableadd.html', context)

def operatortableaddsubmit(request):
    context = {}
    form = WinchOperatorTableForm(request.POST)
    context['form'] = form
    if form.is_valid():
        context['winchoperator'] = form.save()
    else:
        return render(request, 'wwdb/configuration/operatortableadd.html', context)
    return render(request, 'wwdb/configuration/operatortablerow.html', context)

def operatortableaddcancel(request):
    return HttpResponse()

def operatortabledelete(request, winchoperator_pk):
    winchoperator = WinchOperator.objects.get(pk=winchoperator_pk)
    winchoperator.delete()
    return HttpResponse()

def operatortableedit(request, winchoperator_pk):
    winchoperator = WinchOperator.objects.get(pk=winchoperator_pk)
    context = {}
    context['winchoperator'] = winchoperator
    context['form'] = WinchOperatorTableForm(initial={
        'firstname':winchoperator.firstname,
        'lastname': winchoperator.lastname,
        'status': winchoperator.status,
        'username': winchoperator.username,
    })
    return render(request, 'wwdb/configuration/operatortableedit.html', context)

def operatortableeditsubmit(request, winchoperator_pk):
    context = {}
    winchoperator = WinchOperator.objects.get(pk=winchoperator_pk)
    context['winchoperator'] = winchoperator
    if request.method == 'POST':
        form = WinchOperatorTableForm(request.POST, instance=winchoperator)
        if form.is_valid():
            form.save()
        else:
            return render(request, 'wwdb/configuration/operatortableedit.html', context)
    return render(request, 'wwdb/configuration/operatortablerow.html', context)

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
            return HttpResponseRedirect("/wwdb/configuration/castconfiguration")
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
            return HttpResponseRedirect("/wwdb/configuration/castconfiguration")
    else:
        form = AddOperatorForm 
        if 'submitted' in request.GET:
            submitted = True
            return render(request, 'wwdb/configuration/operatoradd.html', {'form':form, 'submitted':submitted, 'id':id})

    context['form']= form

    return render(request, 'wwdb/configuration/deploymentadd.html', context)

"""
CALIBRATIONS
Classes related to calibrations
"""

class CalibrationDelete(DeleteView):
    model = Calibration
    template_name="wwdb/maintenance/calibrationdelete.html"
    success_url= reverse_lazy('calibrationlist')

def calibrationdetail(request, pk):
    calibration = get_object_or_404(Calibration, id=pk)

    def add_error_fields(queryset):
        for obj in queryset:
            try:
                applied = float(obj.appliedload)
                tension = float(obj.loadcelltension)
                error_lbs = tension - applied
                error_pct = (error_lbs / applied * 100) if applied != 0 else None
            except (TypeError, ZeroDivisionError, ValueError):
                error_lbs = None
                error_pct = None
            obj.error_lbs = error_lbs
            obj.error_pct = error_pct
        return queryset

    tension_verifications = add_error_fields(TensionVerification.objects.filter(calibration=calibration))
    tension_calibrations = add_error_fields(TensionCalibration.objects.filter(calibration=calibration))
    calibration_verifications = add_error_fields(CalibrationVerification.objects.filter(calibration=calibration))

    return render(request, 'wwdb/maintenance/calibrationdetail.html', {
        'calibration': calibration,
        'tension_verifications': tension_verifications,
        'tension_calibrations': tension_calibrations,
        'calibration_verifications': calibration_verifications,
    })

def calibrationedit(request, pk):
    calibration = get_object_or_404(Calibration, id=pk)

    formset1 = TensionVerificationFormSet(
        request.POST or None,
        queryset=TensionVerification.objects.filter(calibration=calibration),
        prefix='tv1'
    )
    formset2 = TensionCalibrationFormSet(
        request.POST or None,
        queryset=TensionCalibration.objects.filter(calibration=calibration),
        prefix='tc1'
    )
    formset3 = CalibrationVerificationFormSet(
        request.POST or None,
        queryset=CalibrationVerification.objects.filter(calibration=calibration),
        prefix='cv1'
    )

    if request.method == 'POST':
        if formset1.is_valid() and formset2.is_valid() and formset3.is_valid():
            instances1 = formset1.save(commit=False)
            instances2 = formset2.save(commit=False)
            instances3 = formset3.save(commit=False)

            # Reassign calibration FK before saving
            for instance in instances1 + instances2 + instances3:
                instance.calibration = calibration
                instance.save()

            return redirect('calibrationdetail', pk=calibration.id)

    return render(request, 'wwdb/maintenance/calibrationedit.html', {
        'calibration': calibration,
        'formset1': formset1,
        'formset2': formset2,
        'formset3': formset3,
    })

def calibrationlist(request):
    calibrations=Calibration.objects.all()
    context={
        'calibrations': calibrations,
        }
    return render(request, 'wwdb/maintenance/calibrationlist.html', context)

def calibrationlogsheet(request, pk):
    calibration = Calibration.objects.get(id=pk)

    formset1 = TensionVerificationFormSet(request.POST or None, queryset=TensionVerification.objects.none(), prefix='tv1')
    formset2 = TensionCalibrationFormSet(request.POST or None, queryset=TensionCalibration.objects.none(), prefix='tc1')
    formset3 = CalibrationVerificationFormSet(request.POST or None, queryset=CalibrationVerification.objects.none(), prefix='cv1')

    for formset in [formset1, formset2, formset3]:
        for form in formset:
            form.fields['appliedload'].widget.attrs.update({'class': 'appliedload form-control'})
            form.fields['loadcelltension'].widget.attrs.update({'class': 'loadcelltension form-control'})
            form.fields['loadcellrawmv'].widget.attrs.update({'class': 'loadcellrawmv form-control'})

    if request.method == 'POST':
        if formset1.is_valid() and formset2.is_valid() and formset3.is_valid():
            for instances in [formset1.save(commit=False), formset2.save(commit=False), formset3.save(commit=False)]:
                for instance in instances:
                    instance.calibration = calibration
                    instance.save()
            return redirect('calibrationlist')


    return render(request, 'wwdb/maintenance/calibrationlogsheet.html', {
        'formset1': formset1,
        'formset2': formset2,
        'formset3': formset3,
        'calibration': calibration,
    })


def calibrationworksheet(request):

    form = CalibrationWorksheetForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)  
            obj.worksheet_calculation()
            obj.save()
            return redirect('calibrationlogsheet', pk=obj.id)

    context = {
        'form':form,
    }

    return render(request, "wwdb/maintenance/calibrationworksheet.html", context)

def calibrationeditdetails(request, pk):
    calibration = get_object_or_404(Calibration, pk=pk)
    form = CalibrationWorksheetForm(request.POST or None, instance=calibration)

    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            obj.worksheet_calculation()
            obj.save()
            return redirect('calibrationdetail', pk=obj.id)

    context = {
        'form': form,
        'calibration': calibration,
    }

    return render(request, "wwdb/maintenance/calibrationeditdetails.html", context)


"""
DEPLOYMENTS 
Classes related to create, update, view DeploymentType model
"""

def deploymenttablelistget(request):
    context = {}
    context['deployment'] = DeploymentType.objects.all()
    return render(request, 'wwdb/configuration/deploymenttablelist.html', context)

def deploymenttableadd(request):
    context = {'form': DeploymentTableForm()}
    return render(request, 'wwdb/configuration/deploymenttableadd.html', context)

def deploymenttableaddsubmit(request):
    context = {}
    form = DeploymentTableForm(request.POST)
    context['form'] = form
    if form.is_valid():
        context['deployment'] = form.save()
    else:
        return render(request, 'wwdb/configuration/deploymenttableadd.html', context)
    return render(request, 'wwdb/configuration/deploymenttablerow.html', context)

def deploymenttableaddcancel(request):
    return HttpResponse()

def deploymenttabledelete(request, deployment_pk):
    deployment = DeploymentType.objects.get(pk=deployment_pk)
    deployment.delete()
    return HttpResponse()

def deploymenttableedit(request, deployment_pk):
    deployment = DeploymentType.objects.get(pk=deployment_pk)
    context = {}
    context['deployment'] = deployment
    context['form'] = DeploymentTableForm(initial={
        'status':deployment.status,
        'name': deployment.name,
        'equipment': deployment.equipment,
        'notes': deployment.notes,
    })
    return render(request, 'wwdb/configuration/deploymenttableedit.html', context)

def deploymenttableeditsubmit(request, deployment_pk):
    context = {}
    deployment = DeploymentType.objects.get(pk=deployment_pk)
    context['deployment'] = deployment
    if request.method == 'POST':
        form = DeploymentTableForm(request.POST, instance=deployment)
        if form.is_valid():
            form.save()
        else:
            return render(request, 'wwdb/configuration/deploymenttableedit.html', context)
    return render(request, 'wwdb/configuration/deploymenttablerow.html', context)

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
            return HttpResponseRedirect("/wwdb/configuration/castconfiguration")
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
            return HttpResponseRedirect("/wwdb/configuration/castconfiguration")
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

    return render(request, 'wwdb/maintenance/breaktestlist.html', context)

def breaktestadd(request):
    context ={}
    form = BreaktestAddForm(request.POST or None)
    if request.method == "POST":
        form = BreaktestAddForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/wwdb/maintenance/breaktestlist')
    else:
        form = BreaktestAddForm
        if 'submitted' in request.GET:
            submitted = True
            return render(request, 'wwdb/maintenance/breaktestadd.html', {'form':form, 'submitted':submitted, 'id':id})
 
    context['form']= form

    return render(request, "wwdb/maintenance/breaktestadd.html", context)

def breaktestedit(request, id):
    context ={}
    obj = get_object_or_404(Breaktest, id = id)

    if request.method == 'POST':
        form = BreaktestEditForm(request.POST, instance = obj)
        if form.is_valid():
            form.save()
            breaktestid=Breaktest.objects.get(id=id)
            return HttpResponseRedirect("/wwdb/maintenance/breaktestlist")
    else:
        form = BreaktestEditForm(instance = obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/wwdb/maintenance/breaktest/%i/edit" % breaktestid.pk)

    context["form"] = form
    return render(request, "wwdb/maintenance/lubricationedit.html", context)

class BreaktestDelete(DeleteView):
    model = Breaktest
    template_name="wwdb/maintenance/breaktestdelete.html"
    success_url= reverse_lazy('breaktestlist')



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

class CutbackreterminationDelete(DeleteView):
    model = CutbackRetermination
    template_name="wwdb/maintenance/cutbackreterminationdelete.html"
    success_url= reverse_lazy('cutbackreterminationlist')


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

def cruisetablelistget(request):
    context = {}
    context['cruise'] = Cruise.objects.all()
    return render(request, 'wwdb/configuration/cruisetablelist.html', context)

def cruisetableadd(request):
    context = {'form': CruiseTableForm()}
    return render(request, 'wwdb/configuration/cruisetableadd.html', context)

def cruisetableaddsubmit(request):
    context = {}
    form = CruiseTableForm(request.POST)
    context['form'] = form
    if form.is_valid():
        context['cruise'] = form.save()
    else:
        return render(request, 'wwdb/configuration/cruisetableadd.html', context)
    return render(request, 'wwdb/configuration/cruisetablerow.html', context)

def cruisetableaddcancel(request):
    return HttpResponse()

def cruisetabledelete(request, cruise_pk):
    cruise = Cruise.objects.get(pk=cruise_pk)
    cruise.delete()
    return HttpResponse()

def cruisetableedit(request, cruise_pk):
    cruise = Cruise.objects.get(pk=cruise_pk)
    context = {}
    context['cruise'] = cruise
    context['form'] = CruiseTableForm(initial={
        'number':cruise.number,
        'startdate': cruise.startdate,
        'enddate': cruise.enddate,
    })
    return render(request, 'wwdb/configuration/cruisetableedit.html', context)

def cruisetableeditsubmit(request, cruise_pk):
    context = {}
    cruise = Cruise.objects.get(pk=cruise_pk)
    context['cruise'] = cruise
    if request.method == 'POST':
        form = CruiseTableForm(request.POST, instance=cruise)
        if form.is_valid():
            form.save()
        else:
            return render(request, 'wwdb/configuration/cruisetablerow.html', context)
    return render(request, 'wwdb/configuration/cruisetablerow.html', context)

def cruiseedit(request, id):
    context ={}
    obj = get_object_or_404(Cruise, id = id)

    if request.method == 'POST':
        form = EditCruiseForm(request.POST, instance = obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/wwdb/configuration/castconfiguration/#cruise")
    else:
        form = EditCruiseForm(instance = obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/wwdb/configuration/cruise/%i/edit" % obj.pk)

    context ={}
    context["form"] = form
    return render(request, "wwdb/configuration/cruiseedit.html", context)

def cruiseadd(request):
    context ={}
    form = EditCruiseForm(request.POST or None)
    if request.method == "POST":
        form = EditCruiseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            cruiseid=Cruise.objects.last()
            return HttpResponseRedirect("/wwdb/configuration/cruiseconfiguration/")
    else:
        form = EditCruiseForm 
        if 'submitted' in request.GET:
            submitted = True
            return render(request, 'wwdb/configuration/cruiseadd.html', {'form':form, 'submitted':submitted, 'id':id})

    context['form']= form

    return render(request, 'wwdb/configuration/cruiseadd.html', context)

def cruiseeditmeta(request, pk):
    obj = get_object_or_404(Cruise, id = pk)

    winch1status=obj.winch1status
    winch2status=obj.winch2status
    winch3status=obj.winch3status

    if request.method == 'POST':
        form = EditCruiseMetaForm(request.POST, instance = obj)
        if form.is_valid():
            form.save()
            cruiseid=Cruise.objects.get(id=pk)
            return HttpResponseRedirect("/wwdb/configuration/castconfiguration")
    else:
        form = EditCruiseMetaForm(instance = obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/wwdb/configuration/cruise/%i/cruiseeditmeta" % cruiseid.pk)
    
    context ={
        'winch1status':winch1status,
        'winch2status':winch2status,
        'winch3status':winch3status,
        }

    context["form"] = form
    return render(request, "wwdb/configuration/cruiseeditmeta.html", context)


"""
LUBRICATION
Classes related to create, update, view Lubrication model
"""

def lubricationlist(request):
    lubrication = Lubrication.objects.order_by('-date')

    context = {
        'lubrication': lubrication, 
        }

    return render(request, 'wwdb/maintenance/lubricationlist.html', context=context)

def lubricationadd(request):
    context ={}
    form = LubricationAddForm(request.POST or None)
    if request.method == "POST":
        form = LubricationAddForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/wwdb/maintenance/lubricationlist')
    else:
        form = LubricationAddForm
        if 'submitted' in request.GET:
            submitted = True
            return render(request, 'wwdb/maintenance/lubricationadd.html', {'form':form, 'submitted':submitted, 'id':id})
 
    context['form']= form

    return render(request, "wwdb/maintenance/lubricationadd.html", context)

def lubricationdetail(request, id):
    context ={}
    context["lubrication"] = Lubrication.objects.get(id = id)     
    return render(request, "wwdb/maintenance/lubricationdetail.html", context)

def lubricationedit(request, id):
    context ={}
    obj = get_object_or_404(Lubrication, id = id)

    if request.method == 'POST':
        form = LubricationEditForm(request.POST, instance = obj)
        if form.is_valid():
            form.save()
            lubricationid=Lubrication.objects.get(id=id)
            return HttpResponseRedirect("/wwdb/maintenance/lubricationlist")
    else:
        form = LubricationEditForm(instance = obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/wwdb/maintenance/lubrication/%i/edit" % lubricationid.pk)

    context["form"] = form
    return render(request, "wwdb/maintenance/lubricationedit.html", context)

class LubricationDelete(DeleteView):
    model = Lubrication
    template_name="wwdb/maintenance/lubricationdelete.html"
    success_url= reverse_lazy('lubricationlist')

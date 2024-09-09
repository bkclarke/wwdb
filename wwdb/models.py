from types import NoneType
from django.db import models
from django.db.models.query_utils import select_related_descend
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Avg, Count, Min, Sum, Max
from django.core.validators import MaxValueValidator
from datetime import datetime, date
from pandas.core.base import NoNewAttributesMixin
from django.utils.dateparse import parse_datetime
import pyodbc 
import pandas as pd


def validate_commas(value):
    if "," in value:
        raise ValidationError("Invalid entry: remove commas")
    else:
        return

class Breaktest(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  
    wire = models.ForeignKey('Wire', models.DO_NOTHING, db_column='WireId', blank=True, null=True, verbose_name='Wire', related_name='wire_break_test')  
    date = models.DateField(db_column='Date', blank=True, null=True, verbose_name='Date', validators=[MaxValueValidator(limit_value=date.today)])  
    testedbreakingload = models.IntegerField(db_column='TestedBreakingLoad', blank=True, null=True, verbose_name='Tested breaking load')  
    notes = models.TextField(db_column='Notes', blank=True, null=True, verbose_name='Notes', validators=[validate_commas])  

    class Meta:
        managed = True
        db_table = 'BreakTest'
        verbose_name_plural = "BreakTest"

    def __str__(self):
        return str(self.date)

    @property
    def format_date(self):
        date=self.date
        formatdate=date.strftime("%Y-%m-%d")
        return formatdate

class Calibration(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  
    appliedloadlow = models.IntegerField(db_column='AppliedLoadLow', blank=True, null=True, verbose_name='Lowest applied load')  
    tensionlow = models.IntegerField(db_column='TensionLow', blank=True, null=True, verbose_name='Lowest tension')  
    rawmvlow = models.FloatField(db_column='RawmVLow', blank=True, null=True, verbose_name='Lowest raw mv')  
    appliedloadhigh = models.IntegerField(db_column='AppliedLoadHigh', blank=True, null=True, verbose_name='Highest applied load')  
    tensionhigh = models.IntegerField(db_column='TensionHigh', blank=True, null=True, verbose_name='Highest tension')  
    rawmvhigh = models.FloatField(db_column='RawmVHigh', blank=True, null=True, verbose_name='Highest raw mv')  
    calibration = models.ForeignKey('CalibrationMeta', models.DO_NOTHING, db_column='CalibrationId', blank=True, null=True, verbose_name='Calibration id')  

    class Meta:
        managed = True
        db_table = 'Calibration'
        verbose_name_plural = "Calibration"


class CalibrationMeta(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  
    winch = models.ForeignKey('Winch', models.DO_NOTHING, db_column='WinchId', blank=True, null=True, verbose_name='Winch')  
    date = models.DateField(db_column='Date', blank=True, null=True, verbose_name='Date', validators=[MaxValueValidator(limit_value=date.today)])  
    operator = models.ForeignKey('Winchoperator', models.DO_NOTHING, db_column='OperatorId', blank=True, null=True, verbose_name='Operator')  
    wire = models.ForeignKey('Wire', models.DO_NOTHING, db_column='WireId', blank=True, null=True, verbose_name='Wire id')  
    dynomometerid = models.ForeignKey('Dynomometer', models.DO_NOTHING, db_column='DynomometerId', blank=True, null=True, verbose_name='Dynomometer')  
    frame = models.ForeignKey('Frame', models.DO_NOTHING, db_column='FrameId', blank=True, null=True, verbose_name='Frame')  
    safetyfactor = models.IntegerField(db_column='SafetyFactor', blank=True, null=True, verbose_name='Factor of safety')  
    monitoringaccuracy = models.IntegerField(db_column='MonitoringAccuracy', blank=True, null=True, verbose_name='Monitoring accuracy')  

    class Meta:
        managed = True
        db_table = 'CalibrationMeta'
        verbose_name_plural = "CalibrationMeta"

    def __str__(self):
        return str(self.date)


class Cast(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  
    startoperator = models.ForeignKey('WinchOperator', models.DO_NOTHING, db_column='StartOperatorId', null=True, related_name='startoperatorid', verbose_name="Start operator")  
    endoperator = models.ForeignKey('WinchOperator', models.DO_NOTHING, db_column='EndOperatorId', null=True, related_name='endoperatorid', verbose_name='End operator')  
    startdate = models.DateTimeField(db_column='StartDate', blank=True, null=True, verbose_name='Start date and time', validators=[MaxValueValidator(limit_value=datetime.today)])  
    enddate = models.DateTimeField(db_column='EndDate', blank=True, null=True, verbose_name='End date and time', validators=[MaxValueValidator(limit_value=datetime.today)])  
    deploymenttype = models.ForeignKey('Deploymenttype', models.DO_NOTHING, db_column='DeploymentTypeId', null=True, verbose_name='Deployment type')  
    wire = models.ForeignKey('Wire', models.DO_NOTHING, db_column='WireId', blank=True, null=True, verbose_name='Wire')  
    winch = models.ForeignKey('Winch', models.DO_NOTHING, db_column='WinchId', related_name='cast_winch', null=True, verbose_name='Winch')  
    notes = models.TextField(db_column='Notes', blank=True, null=True, verbose_name='Notes', validators=[validate_commas])  
    maxtension = models.IntegerField(db_column='MaxTension', blank=True, null=True, verbose_name='Max tension')  
    maxpayout = models.IntegerField(db_column='MaxPayout', blank=True, null=True, verbose_name='Max payout')  
    payoutmaxtension = models.IntegerField(db_column='PayoutMaxTension', blank=True, null=True, verbose_name='Payout at max tension')  
    metermaxtension = models.IntegerField(db_column='MeterMaxTension', blank=True, null=True, verbose_name='Meter mark at max tension')  
    timemaxtension = models.DateTimeField(db_column='TimeMaxTension', blank=True, null=True, verbose_name='Time at max tension')  
    flagforreview = models.BooleanField(db_column='Flagforreview', blank=True, null=True, verbose_name='Flag for review')  
    dryendtag = models.IntegerField(db_column='DryEndTag', blank=True, null=True, verbose_name='Dry end tag')  
    wetendtag = models.IntegerField(db_column='WetEndTag', blank=True, null=True, verbose_name='Wet end tag')  
    motor = models.ForeignKey('Motor', models.DO_NOTHING, db_column='MotorId', blank=True, null=True, verbose_name='Motor')
    wirerinse = models.BooleanField(db_column='wirerinse', blank=True, null=True, verbose_name='Wire rinse')  
    wirelength = models.IntegerField(db_column='WireLength', blank=True, null=True, verbose_name='Wire length')  
    factorofsafety = models.FloatField(db_column='FactorofSafety', blank=False, null=True, verbose_name='Factor of safety')  
    safeworkingtension = models.FloatField(db_column='SafeWorkingTension', blank=False, null=True, verbose_name='Safe Working tension')  
    duration = models.IntegerField(db_column='Duration', blank=True, null=True, verbose_name='Duration')  


    class Meta:
        managed = True
        db_table = 'Cast'
        verbose_name_plural = "Cast"

    def get_absolute_url(self):
        return reverse('castdetail', kwargs={'pk':self.pk})

    def __str__(self):
        return str(self.startdate)


    @property
    def dry_end_tag(self):
        winch=self.winch
        wire=winch.reverse_wire.last()
        dryend=wire.dryendtag
        return dryend

    @property
    def wet_end_tag(self):
        winch=self.winch
        wire=winch.reverse_wire.last()
        wetend=wire.active_wetendtag
        return wetend

    @property
    def active_winch(self):
        d=self.winch.name
        return d

    @property
    def active_wire(self):
        if self.winch:
            d=self.winch.active_wire.wireid
        return d

    @property
    def active_wire_length(self):
        if self.active_wire:
            d=self.active_wire.active_length
        return d

    @property
    def active_wire_safeworkingtension(self):
        if self.active_wire:
            d=self.active_wire.safe_working_tension
        return d

    @property
    def active_wire_factorofsafety(self):
        if self.active_wire:
            d=self.active_wire.factorofsafety 
        return d
		
    @property
    def active_motor(self):
        if not self.motor:
            return
        d=self.motor.number
        return d

    @property
    def format_startdate(self):
        if self.startdate:
            date=self.startdate
            formatdate=date.strftime("%Y-%m-%d %H:%M:%S")
            return formatdate
        return

    @property
    def format_timemaxtension(self):
        if not self.timemaxtension:
            return
        date=self.timemaxtension
        formatdate=date.strftime("%Y-%m-%d %H:%M:%S")
        return formatdate

    @property
    def active_wire(self):
        winch=self.winch
        wire=winch.reverse_wire.last()
        return wire

    def get_active_wire(self):
        if self.active_wire:
            self.wire=self.active_wire
        return

    def get_active_length(self):
        if self.active_wire_length:
            self.wirelength=self.active_wire_length
        return

    def get_active_factorofsafety(self):
        if self.active_wire_factorofsafety:
            self.factorofsafety=self.active_wire_factorofsafety.factorofsafety
        return

    def get_active_safeworkingtension(self):
        if self.active_wire_safeworkingtension:
            self.safeworkingtension=self.active_wire_safeworkingtension
        return

    def endcastcal(self):
        winch=(self.winch.name)
        if winch=='winch1' or winch=='winch2' or winch=='winch3':
            try:
                conn = pyodbc.connect('Driver={SQL Server};'
                                        'Server=192.168.1.90, 1433;'
                                        'Database=WinchDb;'
                                        'Trusted_Connection=no;'
			                    'UID=remoteadmin;'
			                    'PWD=eris.2003;')

                winch=(self.winch.name)
                startcal=str(self.startdate)
                startcal=startcal[:19]
                endcal=str(self.enddate)
                endcal=endcal[:19]
                df=pd.read_sql_query("SELECT * FROM " + winch + " WHERE DateTime BETWEEN '" + startcal + "' AND '" + endcal + "'", conn)
                castmaxtensiondf=df[df.Tension==df.Tension.max()]
                castmaxtension=castmaxtensiondf['Tension'].max()
                castmaxpayout=df['Payout'].max()
                castpayoutmaxtension=castmaxtensiondf['Payout'].max()
                casttimemaxtension=castmaxtensiondf['DateTime'].max()

                conn.close()

                wetend=int(self.wet_end_tag)
                dryend=int(self.dry_end_tag)

                if castpayoutmaxtension<0:
                    payout=0
                else:
                    payout=castpayoutmaxtension

                if wetend>dryend:
                    length=int(wetend)-int(payout)
                    castmetermaxtension=length
                else:
                    length=int(wetend)+int(payout)
                    castmetermaxtension=length

                self.maxtension=castmaxtension
                self.maxpayout=castmaxpayout
                self.payoutmaxtension=castpayoutmaxtension
                self.timemaxtension=casttimemaxtension
                self.metermaxtension=castmetermaxtension
                self.wetendtag=wetend
                self.dryendtag=dryend

            except :
                wetend=int(self.wet_end_tag)
                dryend=int(self.dry_end_tag)
                self.wetendtag=wetend
                self.dryendtag=dryend
                return

        else:
            return

    def startcast_get_datetime(self):
        if self.startdate is None:
            current_datetime = datetime.now()
            self.startdate = current_datetime

    def endcast_get_datetime(self):
        if self.enddate is None:
            current_datetime = datetime.now()
            self.enddate = current_datetime

    def get_cast_duration(self):
        if self.enddate and self.startdate:
            start = self.startdate
            end = self.enddate
            duration = (end - start)
            duration_in_minutes = round(duration.total_seconds() / 60)
            self.duration = duration_in_minutes

class Cruise(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)   
    number = models.TextField(db_column='Number', blank=True, null=True, verbose_name='Cruise number', validators=[validate_commas])   
    startdate = models.DateField(db_column='StartDate', blank=True, null=True, verbose_name='Start date')   
    enddate = models.DateField(db_column='EndDate', blank=True, null=True, verbose_name='End date')   
    winch1status = models.BooleanField(db_column='Winch1Status', blank=True, null=True, verbose_name='Winch 1 status', validators=[validate_commas])   
    winch2status = models.BooleanField(db_column='Winch2Status', blank=True, null=True, verbose_name='Winch 2 status', validators=[validate_commas])   
    winch3status = models.BooleanField(db_column='Winch3Status', blank=True, null=True, verbose_name='Winch 3 status', validators=[validate_commas])   
    winch1blockarrangement = models.TextField(db_column='Winch1BlockArrangement', blank=True, null=True, verbose_name='Winch 1 Block Arrangement', validators=[validate_commas])   
    winch2blockarrangement = models.TextField(db_column='Winch2BlockArrangement', blank=True, null=True, verbose_name='Winch 2 Block Arrangement', validators=[validate_commas])   
    winch3blockarrangement = models.TextField(db_column='Winch3BlockArrangement', blank=True, null=True, verbose_name='Winch 3 Block Arrangement', validators=[validate_commas])   
    winch1termination = models.TextField(db_column='Winch1Termination', blank=True, null=True, verbose_name='Winch 1 Termination', validators=[validate_commas])   
    winch2termination = models.TextField(db_column='Winch2Termination', blank=True, null=True, verbose_name='Winch 2 Termination', validators=[validate_commas])   
    winch3termination = models.TextField(db_column='Winch3Termination', blank=True, null=True, verbose_name='Winch 3 Termination', validators=[validate_commas])   
    winch2spindirection = models.TextField(db_column='Winch2SpinDirection', blank=True, null=True, verbose_name='Winch 3 Spin Direction', validators=[validate_commas])   
    winch1notes = models.TextField(db_column='Winch1Notes', blank=True, null=True, verbose_name='Winch 1 Notes', validators=[validate_commas])   
    winch2notes = models.TextField(db_column='Winch2Notes', blank=True, null=True, verbose_name='Winch 2 Notes', validators=[validate_commas])   
    winch3notes = models.TextField(db_column='Winch3Notes', blank=True, null=True, verbose_name='Winch 3 Notes', validators=[validate_commas])   
    scienceprovidedwinch = models.TextField(db_column='ScienceProvidedWinch', blank=True, null=True, verbose_name='Science Provided Winch', validators=[validate_commas])   

    class Meta:
        managed = True
        db_table = 'Cruise'
        verbose_name_plural = 'cruise'

    def __str__(self):
        return str(self.number)

    @property
    def format_startdate(self):
        if self.startdate:
            date=self.startdate
            formatdate=date.strftime("%Y-%m-%d")
            return formatdate

    @property
    def format_enddate(self):
        if not self.enddate:
            return
        date=self.enddate
        formatdate=date.strftime("%Y-%m-%d")
        return formatdate

class CutbackRetermination(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  
    wetendtag = models.IntegerField(db_column='WetEndTag', blank=True, null=True, verbose_name='Wet end tag value (m)')  
    dryendtag = models.IntegerField(db_column='DryEndTag', blank=True, null=True, verbose_name='Dry end tag value (m)')  
    wire = models.ForeignKey('Wire', models.DO_NOTHING, db_column='WireId', blank=True, null=True, related_name='wire_cutback_retermination', verbose_name='Wire')  
    notes = models.TextField(db_column='Notes', blank=True, null=True, verbose_name='Notes')  
    date = models.DateField(db_column='Date', blank=True, null=True, verbose_name='Date', validators=[MaxValueValidator(limit_value=date.today)])
    lengthaftercutback = models.IntegerField(db_column='LengthAfterCutback', blank=True, null=True, verbose_name='Length after cutback')  

    class Meta:
        managed = True
        db_table = 'CutbackRetermination'
        verbose_name_plural = "CutbackRetermination"

    def __str__(self):
        return str(self.date)

    @property
    def wire_dry_end_tag(self):
        w=self.wire.dryendtag
        return w

    @property
    def length(self):
        dryendlength=self.wire_dry_end_tag
        wetendlength=self.wetendtag
        length=wetendlength-dryendlength
        return length

    @property
    def format_date(self):
        date=self.date
        formatdate=date.strftime("%Y-%m-%d")
        return formatdate

    def submit_length(self):
        if not self.wire_dry_end_tag and self.wetendtag:
            return
        else:
            dryendlength=self.wire_dry_end_tag
            wetendlength=self.wetendtag
            length=wetendlength-dryendlength
            self.lengthaftercutback=abs(int(length))
            return

    def submit_dry_end_tag(self):
        if not self.wire_dry_end_tag:
            return
        else:
            dryendtag=self.wire_dry_end_tag
            self.dryendtag=dryendtag
            return

    def edit_length(self):
        if not self.dryendtag and self.wetendtag:
            return
        else:
            dryendlength=self.dryendtag
            wetendlength=self.wetendtag
            length=wetendlength-dryendlength
            self.lengthaftercutback=abs(int(length))
            return

class DeploymentType(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  
    status = models.BooleanField(db_column='Status', blank=True, null=True, verbose_name='Status')  
    name = models.TextField(db_column='Name', blank=True, null=True, verbose_name='Name', validators=[validate_commas])
    equipment = models.TextField(db_column='Equipment', blank=True, null=True, verbose_name='Equipment', validators=[validate_commas])  
    notes = models.TextField(db_column='Notes', blank=True, null=True, verbose_name='Notes', validators=[validate_commas])  

    class Meta:
        managed = True
        db_table = 'DeploymentType'
        verbose_name_plural = "DeploymentType"
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('deploymentdetail', kwargs={'pk':self.pk})

    def __str__(self):
        return str(self.name)

class Location(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  
    location = models.TextField(db_column='Location', blank=True, null=True, verbose_name='Location', validators=[validate_commas])  

    class Meta:
        managed = True
        db_table = 'Location'
        verbose_name_plural = "Location"
        ordering = ['location']


    def __str__(self):
        return str(self.location)
		
class Motor(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  
    number = models.IntegerField(db_column='Number', blank=True, null=True, verbose_name='Number')  

    class Meta:
        managed = True
        db_table = 'Motor'
        verbose_name_plural = "Motor"

    def __str__(self):
        return str(self.number)

class Drum(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  
    internalid = models.TextField(db_column='InternalId', blank=True, null=True, verbose_name='Internal id', validators=[validate_commas])  
    color = models.TextField(db_column='Color', blank=True, null=True, verbose_name='Color', validators=[validate_commas])  
    size = models.TextField(db_column='Size', blank=True, null=True, verbose_name='Size', validators=[validate_commas])  
    weight = models.TextField(db_column='Weight', blank=True, null=True, verbose_name='Weight', validators=[validate_commas])  
    location = models.ManyToManyField(Location, through='DrumLocation', related_name='active_location', verbose_name='Location')
    #wire = models.ManyToManyField(Wire, through='Wiredrum', related_name='active_wire', verbose_name='Wire')
    material = models.TextField(db_column='Material', blank=True, null=True, verbose_name='Material', validators=[validate_commas])  
    wiretype = models.TextField(db_column='WireType', blank=True, null=True, verbose_name='Wire type', validators=[validate_commas])    

    class Meta:
        managed = True
        db_table = 'Drum'
        verbose_name_plural = "Drum"

    def __str__(self):
        return str(self.internalid)

    @property
    def active_drum_location(self):
        d=self.drumlocation_set.order_by('-date').first()
        return d

    @property
    def active_location(self):
        d=self.active_drum_location.location
        return d

class Dynomometer(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  
    name = models.TextField(db_column='Name', blank=True, null=True, verbose_name='Name', validators=[validate_commas])  
    dynomometertype = models.TextField(db_column='DynomometerType', blank=True, null=True, verbose_name='Dynomometer type', validators=[validate_commas])  
    comments = models.TextField(db_column='Comments', blank=True, null=True, verbose_name='notes', validators=[validate_commas])  

    class Meta:
        managed = True
        db_table = 'Dynomometer'
        verbose_name_plural = "Dynomometer"

    def __str__(self):
        return str(self.name)

class Frame(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  
    name = models.TextField(db_column='Name', blank=True, null=True, verbose_name='Name', validators=[validate_commas])  
    frametype = models.TextField(db_column='FrameType', blank=True, null=True, verbose_name='Frame type', validators=[validate_commas])  

    class Meta:
        managed = True
        db_table = 'Frame'
        verbose_name_plural = "Frame"

    def __str__(self):
        return str(self.name)




class Lubrication(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  
    wire = models.ForeignKey('Wire', models.DO_NOTHING, db_column='WireId', blank=True, null=True, verbose_name='Wire')  
    lubetype = models.TextField(db_column='LubeType', blank=True, null=True, verbose_name='Lube type', validators=[validate_commas])  
    date = models.DateField(db_column='Date', blank=True, null=True, verbose_name='Date', validators=[MaxValueValidator(limit_value=date.today)])  
    lubelength = models.IntegerField(db_column='LubeLength', blank=True, null=True, verbose_name='Length lubed')
    lubestartmetermark = models.IntegerField(db_column='LubeStartMeterMark', blank=True, null=True, verbose_name='Start meter mark')
    lubeendmetermark = models.IntegerField(db_column='LubeEndMeterMark', blank=True, null=True, verbose_name='End meter mark')
    notes = models.TextField(db_column='Notes', blank=True, null=True, verbose_name='Notes', validators=[validate_commas])  

    class Meta:
        managed = True
        db_table = 'Lubrication'
        verbose_name_plural = "Lubrication"

    def __str__(self):
        return str(self.date)

class FactorOfSafety(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  
    factorofsafety = models.FloatField(db_column='FactorofSafety', blank=False, null=False, default=5.0, verbose_name='Factor of safety')  

    class Meta:
        managed = True
        db_table = 'FactorOfSafety'
        verbose_name_plural = "FactorOfSafety"
        
    def __str__(self):
        return str(self.factorofsafety)

class Winch(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  
    name = models.TextField(db_column='Name', blank=True, null=True, verbose_name='Name', validators=[validate_commas])
    ship = models.TextField(db_column='Ship', blank=True, null=True, verbose_name='Ship', validators=[validate_commas])  
    institution = models.TextField(db_column='Institution', blank=True, null=True, verbose_name='Institution', validators=[validate_commas])  
    manufacturer = models.TextField(db_column='Manufacturer', blank=True, null=True, verbose_name='Manufacturer', validators=[validate_commas])  
    drums = models.ManyToManyField(Drum, through='Drumlocation', related_name='winches', verbose_name='Drum')
    wiretrainschematicjframe = models.TextField(db_column='WireTrainSchematicJFrame', blank=True, null=True, verbose_name='Wire train schematic Jframe', validators=[validate_commas])  
    wiretrainschematicaframe = models.TextField(db_column='WireTrainSchematicAFrame', blank=True, null=True, verbose_name='Wire train schematic Aframe', validators=[validate_commas])  
    status = models.BooleanField(db_column='Status', blank=True, null=True, verbose_name='Status')  

    class Meta:
        managed = True
        db_table = 'Winch'
        verbose_name_plural = "Winch"
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('winchdetail', kwargs={'pk':self.pk})

    def __str__(self):
        return str(self.name)

    @property
    def active_drum(self):
        d=self.drumlocation_set.order_by('date').last()
        return d
        

class WinchOperator(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)    
    status = models.BooleanField(db_column='Status', blank=True, null=True, verbose_name='Status')  
    firstname = models.TextField(db_column='FirstName', blank=True, null=True, verbose_name='First name', validators=[validate_commas])  
    lastname = models.TextField(db_column='LastName', blank=True, null=True, verbose_name='Last name', validators=[validate_commas])  
    username = models.TextField(db_column='UserName', blank=True, null=True, verbose_name='User name', validators=[validate_commas])  


    class Meta:
        managed = True
        db_table = 'WinchOperator'
        verbose_name_plural = "WinchOperator"
        ordering = ['username']

    def get_absolute_url(self):
        return reverse('operatordetail', kwargs={'pk':self.pk})

    def __str__(self):
        return str(self.username)

class WireRopeData(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  
    name = models.TextField(db_column='Name', blank=True, null=True, verbose_name='Name', validators=[validate_commas])
    manufacturer = models.TextField(db_column='Manufacturer',blank=True, null=True, verbose_name='Manufacturer', validators=[validate_commas])
    manufacturerpartnumber = models.TextField(db_column='ManufacturerPartNumber', blank=True, null=True, verbose_name='Manufacturer part number', validators=[validate_commas])  
    cabletype = models.TextField(db_column='CableType', blank=True, null=True, verbose_name='Cable type', validators=[validate_commas])  
    nominalbreakingload = models.IntegerField(db_column='nominalbreakingload', blank=True, null=True, verbose_name='Nominal breaking load')  
    weightperfoot = models.FloatField(db_column='WeightPerFoot', blank=True, null=True, verbose_name='Weight per foot')  
    
    class Meta:
        managed = True
        db_table = 'WireRopeData'
        verbose_name_plural = 'WireRopeData'

    def __str__(self):
        return str(self.name)

class OwnershipStatus(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)    
    status = models.TextField(db_column='Status', blank=True, null=True, verbose_name='Status')  


    class Meta:
        managed = True
        db_table = 'OwnershipStatus'
        verbose_name_plural = "OwnershipStatus"

    def __str__(self):
        return str(self.status)

class Wire(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  
    wirerope = models.ForeignKey(WireRopeData, models.DO_NOTHING, db_column='WireRopeId', blank=True, null=True, verbose_name='Wire rope data id')  
    winch = models.ForeignKey(Winch, models.DO_NOTHING, db_column='WinchId', blank=True, null=True, verbose_name='Winch', related_name='reverse_wire')  
    manufacturerid = models.TextField(db_column='ManufacturerId', blank=True, null=True, verbose_name='Manufacturer id', validators=[validate_commas])  
    nsfid = models.TextField(db_column='NsfId', blank=True, null=True, verbose_name='NSF id', validators=[validate_commas])  
    dateacquired = models.DateTimeField(db_column='DateAcquired', blank=True, null=True, verbose_name='Date Acquired', validators=[MaxValueValidator(limit_value=datetime.today)])  
    notes = models.TextField(db_column='Notes', blank=True, null=True, verbose_name='notes', validators=[validate_commas])  
    status = models.BooleanField(db_column='Status', blank=True, null=True, verbose_name='Status')
    ownershipstatus = models.ForeignKey(OwnershipStatus, models.DO_NOTHING, db_column='OwnershipStatusId', blank=True, null=True, verbose_name='Ownership status')  
    drums = models.ManyToManyField(Drum, through='WireDrum', related_name='loaded_wires', verbose_name='Drum')
    factorofsafety = models.ForeignKey(FactorOfSafety, models.DO_NOTHING, db_column='FactorofSafety', blank=True, null=True, related_name='wirefactorofsafety', verbose_name='Factor of safety')  
    dryendtag = models.IntegerField(db_column='DryEndTag', blank=True, null=True, verbose_name='Dry end tag value (m)')  

    class Meta:
        managed = True
        db_table = 'Wire'
        verbose_name_plural = "Wire"


    def get_absolute_url(self):
        return reverse('wiredetail', kwargs={'pk':self.pk})

    def __str__(self):
        return str(self.nsfid)

    @property
    def active_wire_drum(self):
        d=self.wiredrum_set.order_by('date').last()
        return d

    @property
    def active_drum(self):
        if not self.active_wire_drum:
            return None
        d=self.active_wire_drum.drum
        return d

    @property
    def active_drum_location(self):
        if not self.active_drum:
            return None
        d=self.active_drum.active_location
        return d

    @property 
    def active_wire_cutback(self):
        c=self.wire_cutback_retermination.order_by('date').last()
        return c    

    @property
    def active_wetendtag(self):
        if not self.active_wire_cutback:
            return None
        w=self.active_wire_cutback.wetendtag
        return w

    @property 
    def active_length(self):
        if not self.active_wire_cutback:
            return None
        dryend=self.dryendtag
        wetend=self.active_wire_cutback.wetendtag
        length=(wetend-dryend)
        abslength=abs(length)
        return abslength

    @property
    def active_break_test(self):
        b=self.wire_break_test.order_by('date').last()
        return b

    @property
    def tested_breaking_load(self):
        if not self.active_break_test:
            return None
        f=self.active_break_test.testedbreakingload
        return f

    @property
    def nominal_breaking_load(self):
        w=Wire.wirerope.get_object(self)
        n=w.nominalbreakingload
        return n

    @property 
    def absolute_breaking_load(self):
        wire=Wire.wirerope.get_object(self)
        nominal=wire.nominalbreakingload
        if not self.active_break_test:
            return None
        tested=self.active_break_test.testedbreakingload
        if nominal > tested:
            return tested
        else:
            return nominal

    @property 
    def safe_working_tension(self):
        if not self.factorofsafety:
            return None
        if not self.factorofsafety.factorofsafety:
            return None
        if not self.absolute_breaking_load:
            return None
        s=self.factorofsafety.factorofsafety
        i=self.absolute_breaking_load
        swl=i/s 
        swl=int(swl)
        return swl

class DrumLocation(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  
    date= models.DateField(db_column='Date', blank=True, null=True, verbose_name='Date', validators=[MaxValueValidator(limit_value=date.today)])  
    enteredby = models.ForeignKey(User, models.DO_NOTHING, db_column='EnteredBy', blank=True, null=True, verbose_name='Entered by')  
    drumid = models.ForeignKey(Drum, models.DO_NOTHING, db_column='DrumId', blank=True, null=True, verbose_name='Drum')  
    winch = models.ForeignKey(Winch, models.DO_NOTHING, db_column='WinchId', blank=True, null=True, verbose_name='Winch')  
    location = models.ForeignKey(Location, models.DO_NOTHING, db_column='LocationId', blank=True, null=True, verbose_name='Location')  
    notes = models.TextField(db_column='Notes', blank=True, null=True, verbose_name='notes', validators=[validate_commas])  
    wire = models.ForeignKey(Wire, models.DO_NOTHING, db_column='WireId', blank=True, null=True, verbose_name='Wire')  

    class Meta:
        managed = True
        db_table = 'DrumLocation'
        verbose_name_plural = "DrumLocation"
        
    def __str__(self):
        return str(self.location) + '-' + str(self.drumid)

    @property
    def active_wire(self):
        drum=self.drumid
        wiredrum=drum.reverse_drum.last()
        if not wiredrum:
            return None
        else:
            wire=wiredrum.wire
            return wire

    def retain_wire_length(self):
        if not self.active_wire:
            return None
        else:
            wire=self.active_wire
            self.wire=wire
            return

    @property
    def format_date(self):
        if not self.date:
            return None
        else:
            date=self.date
            formatdate=date.strftime("%Y-%m-%d")
            return formatdate

class Wiredrum(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  
    drum = models.ForeignKey(Drum, models.DO_NOTHING, db_column='DrumId', blank=True, null=True, verbose_name='Drum', related_name='reverse_drum')  
    wire = models.ForeignKey(Wire, models.DO_NOTHING, db_column='WireId', blank=True, null=True, verbose_name='Wire')  
    date = models.DateField(db_column='Date', blank=True, null=True, verbose_name='Date', validators=[MaxValueValidator(limit_value=date.today)])  
    notes = models.TextField(db_column='Notes', blank=True, null=True, verbose_name='Notes', validators=[validate_commas])  
    

    class Meta:
        managed = True
        db_table = 'WireDrum'
        verbose_name_plural = "WireDrum"

    def __str__(self):
        return str(self.drum)


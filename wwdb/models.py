from types import NoneType
from django.db import models
from django.db.models.query_utils import select_related_descend
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Avg, Count, Min, Sum, Max
from django.core.validators import MaxValueValidator
from datetime import datetime, date
from pandas.core.base import NoNewAttributesMixin
import pyodbc 
import pandas as pd

#note

class Breaktest(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    wire = models.ForeignKey('Wire', models.DO_NOTHING, db_column='WireId', blank=True, null=True, verbose_name='Wire', related_name='wire_break_test')  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=True, null=True, verbose_name='Date', validators=[MaxValueValidator(limit_value=date.today)])  # Field name made lowercase.
    testedbreakingload = models.IntegerField(db_column='TestedBreakingLoad', blank=True, null=True, verbose_name='Tested breaking load')  # Field name made lowercase.
    notes = models.TextField(db_column='Notes', blank=True, null=True, verbose_name='Notes')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'BreakTest'
        verbose_name_plural = "BreakTest"

    def __str__(self):
        return str(self.date)

class Calibration(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    appliedloadlow = models.IntegerField(db_column='AppliedLoadLow', blank=True, null=True, verbose_name='Lowest applied load')  # Field name made lowercase.
    tensionlow = models.IntegerField(db_column='TensionLow', blank=True, null=True, verbose_name='Lowest tension')  # Field name made lowercase.
    rawmvlow = models.FloatField(db_column='RawmVLow', blank=True, null=True, verbose_name='Lowest raw mv')  # Field name made lowercase.
    appliedloadhigh = models.IntegerField(db_column='AppliedLoadHigh', blank=True, null=True, verbose_name='Highest applied load')  # Field name made lowercase.
    tensionhigh = models.IntegerField(db_column='TensionHigh', blank=True, null=True, verbose_name='Highest tension')  # Field name made lowercase.
    rawmvhigh = models.FloatField(db_column='RawmVHigh', blank=True, null=True, verbose_name='Highest raw mv')  # Field name made lowercase.
    calibration = models.ForeignKey('CalibrationMeta', models.DO_NOTHING, db_column='CalibrationId', blank=True, null=True, verbose_name='Calibration id')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Calibration'
        verbose_name_plural = "Calibration"


class CalibrationMeta(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    winch = models.ForeignKey('Winch', models.DO_NOTHING, db_column='WinchId', blank=True, null=True, verbose_name='Winch')  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=True, null=True, verbose_name='Date', validators=[MaxValueValidator(limit_value=date.today)])  # Field name made lowercase.
    operator = models.ForeignKey('Winchoperator', models.DO_NOTHING, db_column='OperatorId', blank=True, null=True, verbose_name='Operator')  # Field name made lowercase.
    wire = models.ForeignKey('Wire', models.DO_NOTHING, db_column='WireId', blank=True, null=True, verbose_name='Wire id')  # Field name made lowercase.
    dynomometerid = models.ForeignKey('Dynomometer', models.DO_NOTHING, db_column='DynomometerId', blank=True, null=True, verbose_name='Dynomometer')  # Field name made lowercase.
    frame = models.ForeignKey('Frame', models.DO_NOTHING, db_column='FrameId', blank=True, null=True, verbose_name='Frame')  # Field name made lowercase.
    safetyfactor = models.IntegerField(db_column='SafetyFactor', blank=True, null=True, verbose_name='Factor of safety')  # Field name made lowercase.
    monitoringaccuracy = models.IntegerField(db_column='MonitoringAccuracy', blank=True, null=True, verbose_name='Monitoring accuracy')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'CalibrationMeta'
        verbose_name_plural = "CalibrationMeta"

    def __str__(self):
        return str(self.date)


class Cast(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    startoperator = models.ForeignKey('WinchOperator', models.DO_NOTHING, db_column='StartOperatorId', null=True, related_name='startoperatorid', verbose_name="Start operator", limit_choices_to={'status': True})  # Field name made lowercase.
    endoperator = models.ForeignKey('WinchOperator', models.DO_NOTHING, db_column='EndOperatorId', null=True, related_name='endoperatorid', verbose_name='End operator', limit_choices_to={'status': True})  # Field name made lowercase.
    startdate = models.DateTimeField(db_column='StartDate', null=False, verbose_name='Start date and time', validators=[MaxValueValidator(limit_value=datetime.today)])  # Field name made lowercase.
    enddate = models.DateTimeField(db_column='EndDate', blank=True, null=True, verbose_name='End date and time', validators=[MaxValueValidator(limit_value=datetime.today)])  # Field name made lowercase.
    deploymenttype = models.ForeignKey('Deploymenttype', models.DO_NOTHING, db_column='DeploymentTypeId', null=True, verbose_name='Deployment type', limit_choices_to={'status': True})  # Field name made lowercase.
    wire = models.ForeignKey('Wire', models.DO_NOTHING, db_column='WireId', blank=True, null=True, verbose_name='Wire')  # Field name made lowercase.
    winch = models.ForeignKey('Winch', models.DO_NOTHING, db_column='WinchId', null=True, verbose_name='Winch', limit_choices_to={'status': True})  # Field name made lowercase.
    notes = models.TextField(db_column='Notes', blank=True, null=True, verbose_name='Notes')  # Field name made lowercase.
    maxtension = models.IntegerField(db_column='MaxTension', blank=True, null=True, verbose_name='Max tension')  # Field name made lowercase.
    maxpayout = models.IntegerField(db_column='MaxPayout', blank=True, null=True, verbose_name='Max payout')  # Field name made lowercase.
    payoutmaxtension = models.IntegerField(db_column='PayoutMaxTension', blank=True, null=True, verbose_name='Payout at max tension')  # Field name made lowercase.
    metermaxtension = models.IntegerField(db_column='MeterMaxTension', blank=True, null=True, verbose_name='Meter mark at max tension')  # Field name made lowercase.
    timemaxtension = models.DateTimeField(db_column='TimeMaxTension', blank=True, null=True, verbose_name='Time at max tension')  # Field name made lowercase.
    flagforreview = models.BooleanField(db_column='Flagforreview', blank=True, null=True, verbose_name='Flag for review')  # Field name made lowercase.
    dryendtag = models.IntegerField(db_column='DryEndTag', blank=True, null=True, verbose_name='Dry end tag')  # Field name made lowercase.
    wetendtag = models.IntegerField(db_column='WetEndTag', blank=True, null=True, verbose_name='Wet end tag')  # Field name made lowercase.


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

    def endcastcal(self):
        try:
            conn = pyodbc.connect('Driver={SQL Server};'
                                    'Server=192.168.2.5, 1433;'
                                    'Database=WinchDb;'
                                    'Trusted_Connection=no;'
			                'UID=remoteadmin;'
			                'PWD=eris.2003;')

            winch=(self.winch.name)
            startcal=str(self.startdate)
            endcal=str(self.enddate)
            df=pd.read_sql_query("SELECT * FROM " + winch + " WHERE DateTime BETWEEN '" + startcal + "' AND '" + endcal + "'", conn)

            castmaxtensiondf=df[df.Tension==df.Tension.max()]
            castmaxtension=castmaxtensiondf['Tension'].max()
            castmaxpayout=df['Payout'].max()
            castpayoutmaxtension=castmaxtensiondf['Payout'].max()
            casttimemaxtension=castmaxtensiondf['DateTime'].max()

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

class Cruise(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    number = models.TextField(db_column='Number', blank=True, null=True, verbose_name='Cruise number')  # Field name made lowercase.
    startdate = models.DateField(db_column='StartDate', blank=True, null=True, verbose_name='Start date', validators=[MaxValueValidator(limit_value=date.today)])  # Field name made lowercase.
    enddate = models.DateField(db_column='EndDate', blank=True, null=True, verbose_name='End date', validators=[MaxValueValidator(limit_value=date.today)])  # Field name made lowercase.
    status = models.BooleanField(db_column='Status', blank=True, null=True, verbose_name='Status')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Cruise'
        verbose_name_plural = 'cruise'

    def __str__(self):
        return str(self.number)

class CutbackRetermination(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    wetendtag = models.IntegerField(db_column='WetEndTag', blank=True, null=True, verbose_name='Wet end tag value (m)')  # Field name made lowercase.
    lengthremoved = models.IntegerField(db_column='LengthRemoved', blank=True, null=True, verbose_name='Length removed (m)')  # Field name made lowercase.
    wire = models.ForeignKey('Wire', models.DO_NOTHING, db_column='WireId', blank=True, null=True, related_name='wire_cutback_retermination', verbose_name='Wire')  # Field name made lowercase.
    notes = models.TextField(db_column='Notes', blank=True, null=True, verbose_name='Notes')  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=True, null=True, verbose_name='Date', validators=[MaxValueValidator(limit_value=date.today)])  # Field name made lowercase.

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


class DeploymentType(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    status = models.BooleanField(db_column='Status', blank=True, null=True, verbose_name='Status')  # Field name made lowercase.
    name = models.TextField(db_column='Name', blank=True, null=True, verbose_name='Name')
    equipment = models.TextField(db_column='Equipment', blank=True, null=True, verbose_name='Equipment')  # Field name made lowercase.
    notes = models.TextField(db_column='Notes', blank=True, null=True, verbose_name='Notes')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'DeploymentType'
        verbose_name_plural = "DeploymentType"

    def get_absolute_url(self):
        return reverse('deploymentdetail', kwargs={'pk':self.pk})

    def __str__(self):
        return str(self.name)

class Location(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    location = models.TextField(db_column='Location', blank=True, null=True, verbose_name='Location')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Location'
        verbose_name_plural = "Location"

    def __str__(self):
        return str(self.location)

class Drum(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    internalid = models.TextField(db_column='InternalId', blank=True, null=True, verbose_name='Internal id')  # Field name made lowercase.
    color = models.TextField(db_column='Color', blank=True, null=True, verbose_name='Color')  # Field name made lowercase.
    size = models.TextField(db_column='Size', blank=True, null=True, verbose_name='Size')  # Field name made lowercase.
    weight = models.TextField(db_column='Weight', blank=True, null=True, verbose_name='Weight')  # Field name made lowercase.
    location = models.ManyToManyField(Location, through='DrumLocation', related_name='active_location', verbose_name='Location')
    material = models.TextField(db_column='Material', blank=True, null=True, verbose_name='Material')  # Field name made lowercase.
    wiretype = models.TextField(db_column='WireType', blank=True, null=True, verbose_name='Wire type')  # Field name made lowercase. This field type is a guess.

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
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    name = models.TextField(db_column='Name', blank=True, null=True, verbose_name='Name')  # Field name made lowercase.
    dynomometertype = models.TextField(db_column='DynomometerType', blank=True, null=True, verbose_name='Dynomometer type')  # Field name made lowercase.
    comments = models.TextField(db_column='Comments', blank=True, null=True, verbose_name='notes')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Dynomometer'
        verbose_name_plural = "Dynomometer"

    def __str__(self):
        return str(self.name)

class Frame(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    name = models.TextField(db_column='Name', blank=True, null=True, verbose_name='Name')  # Field name made lowercase.
    frametype = models.TextField(db_column='FrameType', blank=True, null=True, verbose_name='Frame type')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Frame'
        verbose_name_plural = "Frame"

    def __str__(self):
        return str(self.name)




class Lubrication(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    wire = models.ForeignKey('Wire', models.DO_NOTHING, db_column='WireId', blank=True, null=True, verbose_name='Wire')  # Field name made lowercase.
    lubetype = models.TextField(db_column='LubeType', blank=True, null=True, verbose_name='Lube type')  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=True, null=True, verbose_name='Date', validators=[MaxValueValidator(limit_value=date.today)])  # Field name made lowercase.
    lubelength = models.IntegerField(db_column='LubeLength', blank=True, null=True, verbose_name='Length lubed')  # Field name made lowercase.
    notes = models.TextField(db_column='Notes', blank=True, null=True, verbose_name='Notes')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Lubrication'
        verbose_name_plural = "Lubrication"

    def __str__(self):
        return str(self.date)

class FactorOfSafety(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    factorofsafety = models.FloatField(db_column='FactorofSafety', blank=False, null=False, default=5.0, verbose_name='Factor of safety')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'FactorOfSafety'
        verbose_name_plural = "FactorOfSafety"
        
    def __str__(self):
        return str(self.factorofsafety)

class Winch(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    name = models.TextField(db_column='Name', blank=True, null=True, verbose_name='Name')
    ship = models.TextField(db_column='Ship', blank=True, null=True, verbose_name='Ship')  # Field name made lowercase.
    institution = models.TextField(db_column='Institution', blank=True, null=True, verbose_name='Institution')  # Field name made lowercase.
    manufacturer = models.TextField(db_column='Manufacturer', blank=True, null=True, verbose_name='Manufacturer')  # Field name made lowercase.
    drums = models.ManyToManyField(Drum, through='Drumlocation', related_name='winches', verbose_name='Drum')
    wiretrainschematicjframe = models.TextField(db_column='WireTrainSchematicJFrame', blank=True, null=True, verbose_name='Wire train schematic Jframe')  # Field name made lowercase.
    wiretrainschematicaframe = models.TextField(db_column='WireTrainSchematicAFrame', blank=True, null=True, verbose_name='Wire train schematic Aframe')  # Field name made lowercase.
    status = models.BooleanField(db_column='Status', blank=True, null=True, verbose_name='Status')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Winch'
        verbose_name_plural = "Winch"

    def get_absolute_url(self):
        return reverse('winchdetail', kwargs={'pk':self.pk})

    def __str__(self):
        return str(self.name)
        
class DrumLocation(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    date= models.DateField(db_column='Date', blank=True, null=True, verbose_name='Date', validators=[MaxValueValidator(limit_value=date.today)])  # Field name made lowercase.
    enteredby = models.ForeignKey(User, models.DO_NOTHING, db_column='EnteredBy', blank=True, null=True, verbose_name='Entered by')  # Field name made lowercase.
    drumid = models.ForeignKey(Drum, models.DO_NOTHING, db_column='DrumId', blank=True, null=True, verbose_name='Drum')  # Field name made lowercase.
    winch = models.ForeignKey(Winch, models.DO_NOTHING, db_column='WinchId', blank=True, null=True, verbose_name='Winch')  # Field name made lowercase.
    location = models.ForeignKey(Location, models.DO_NOTHING, db_column='LocationId', blank=True, null=True, verbose_name='Location')  # Field name made lowercase.
    notes = models.TextField(db_column='Notes', blank=True, null=True, verbose_name='notes')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'DrumLocation'
        verbose_name_plural = "DrumLocation"
        
    def __str__(self):
        return str(self.location) + '-' + str(self.drumid)

class WinchOperator(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase. This field type is a guess.
    status = models.BooleanField(db_column='Status', blank=True, null=True, verbose_name='Status')  # Field name made lowercase.
    firstname = models.TextField(db_column='FirstName', blank=True, null=True, verbose_name='First name')  # Field name made lowercase.
    lastname = models.TextField(db_column='LastName', blank=True, null=True, verbose_name='Last name')  # Field name made lowercase.
    username = models.TextField(db_column='UserName', blank=True, null=True, verbose_name='User name')  # Field name made lowercase.


    class Meta:
        managed = True
        db_table = 'WinchOperator'
        verbose_name_plural = "WinchOperator"

    def get_absolute_url(self):
        return reverse('operatordetail', kwargs={'pk':self.pk})

    def __str__(self):
        return str(self.username)

class WireRopeData(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    name = models.TextField(db_column='Name', blank=True, null=True, verbose_name='Name')
    manufacturer = models.TextField(db_column='Manufacturer',blank=True, null=True, verbose_name='Manufacturer')
    manufacturerpartnumber = models.TextField(db_column='ManufacturerPartNumber', blank=True, null=True, verbose_name='Manufacturer part number')  # Field name made lowercase.
    cabletype = models.TextField(db_column='CableType', blank=True, null=True, verbose_name='Cable type')  # Field name made lowercase.
    nominalbreakingload = models.IntegerField(db_column='nominalbreakingload', blank=True, null=True, verbose_name='Nominal breaking load')  # Field name made lowercase.
    weightperfoot = models.FloatField(db_column='WeightPerFoot', blank=True, null=True, verbose_name='Weight per foot')  # Field name made lowercase.
    
    class Meta:
        managed = True
        db_table = 'WireRopeData'
        verbose_name_plural = 'WireRopeData'

    def __str__(self):
        return str(self.name)

class Wire(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    wirerope = models.ForeignKey(WireRopeData, models.DO_NOTHING, db_column='WireRopeId', blank=True, null=True, verbose_name='Wire rope data id')  # Field name made lowercase.
    winch = models.ForeignKey(Winch, models.DO_NOTHING, db_column='WinchId', blank=True, null=True, verbose_name='Winch', related_name='reverse_wire')  # Field name made lowercase.
    manufacturerid = models.TextField(db_column='ManufacturerId', blank=True, null=True, verbose_name='Manufacturer id')  # Field name made lowercase.
    nsfid = models.TextField(db_column='NsfId', blank=True, null=True, verbose_name='NSF id')  # Field name made lowercase.
    dateacquired = models.DateTimeField(db_column='DateAcquired', blank=True, null=True, verbose_name='Date Acquired', validators=[MaxValueValidator(limit_value=datetime.today)])  # Field name made lowercase.
    notes = models.TextField(db_column='Notes', blank=True, null=True, verbose_name='notes')  # Field name made lowercase.
    status = models.BooleanField(db_column='Status', blank=True, null=True, verbose_name='Status')
    drums = models.ManyToManyField(Drum, through='WireDrum', related_name='loaded_wires', verbose_name='Drum')
    factorofsafety = models.ForeignKey(FactorOfSafety, models.DO_NOTHING, db_column='FactorofSafety', blank=True, null=True, related_name='wirefactorofsafety', verbose_name='Factor of safety')  # Field name made lowercase.
    dryendtag = models.IntegerField(db_column='DryEndTag', blank=True, null=True, verbose_name='Dry end tag value (m)')  # Field name made lowercase.

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
        return swl


class Wiredrum(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    drum = models.ForeignKey(Drum, models.DO_NOTHING, db_column='DrumId', blank=True, null=True, verbose_name='Drum', related_name='reverse_drum')  # Field name made lowercase.
    wire = models.ForeignKey(Wire, models.DO_NOTHING, db_column='WireId', blank=True, null=True, verbose_name='Wire')  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=True, null=True, verbose_name='Date', validators=[MaxValueValidator(limit_value=date.today)])  # Field name made lowercase.
    notes = models.TextField(db_column='Notes', blank=True, null=True, verbose_name='Notes')  # Field name made lowercase.
    

    class Meta:
        managed = True
        db_table = 'WireDrum'
        verbose_name_plural = "WireDrum"

    def __str__(self):
        return str(self.drum)


from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Breaktest(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    wireid = models.ForeignKey('Wire', models.DO_NOTHING, db_column='WireId', blank=True, null=True, verbose_name='Wire')  # Field name made lowercase.
    testdate = models.DateTimeField(db_column='TestDate', blank=True, null=True, verbose_name='Test date')  # Field name made lowercase.
    testedbreakingload = models.IntegerField(db_column='TestedBreakingLoad', blank=True, null=True, verbose_name='Tested breaking load')  # Field name made lowercase.
    notes = models.TextField(db_column='Notes', blank=True, null=True, verbose_name='Notes')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'BreakTest'
        verbose_name_plural = "BreakTest"

    def __str__(self):
        return str(self.testdate)

class Calibration(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    appliedloadlow = models.IntegerField(db_column='AppliedLoadLow', blank=True, null=True, verbose_name='Lowest applied load')  # Field name made lowercase.
    tensionlow = models.IntegerField(db_column='TensionLow', blank=True, null=True, verbose_name='Lowest tension')  # Field name made lowercase.
    rawmvlow = models.FloatField(db_column='RawmVLow', blank=True, null=True, verbose_name='Lowest raw mv')  # Field name made lowercase.
    appliedloadhigh = models.IntegerField(db_column='AppliedLoadHigh', blank=True, null=True, verbose_name='Highest applied load')  # Field name made lowercase.
    tensionhigh = models.IntegerField(db_column='TensionHigh', blank=True, null=True, verbose_name='Highest tension')  # Field name made lowercase.
    rawmvhigh = models.FloatField(db_column='RawmVHigh', blank=True, null=True, verbose_name='Highest raw mv')  # Field name made lowercase.
    calibrationid = models.ForeignKey('CalibrationMeta', models.DO_NOTHING, db_column='CalibrationId', blank=True, null=True, verbose_name='Calibration id')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Calibration'
        verbose_name_plural = "Calibration"


class CalibrationMeta(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    winchid = models.ForeignKey('Winch', models.DO_NOTHING, db_column='WinchId', blank=True, null=True, verbose_name='Winch')  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=True, null=True, verbose_name='Date')  # Field name made lowercase.
    operatorid = models.ForeignKey('Winchoperator', models.DO_NOTHING, db_column='OperatorId', blank=True, null=True, verbose_name='Operator')  # Field name made lowercase.
    wireid = models.ForeignKey('Wire', models.DO_NOTHING, db_column='WireId', blank=True, null=True, verbose_name='Wire id')  # Field name made lowercase.
    dynomometerid = models.ForeignKey('Dynomometer', models.DO_NOTHING, db_column='DynomometerId', blank=True, null=True, verbose_name='Dynomometer')  # Field name made lowercase.
    frameid = models.ForeignKey('Frame', models.DO_NOTHING, db_column='FrameId', blank=True, null=True, verbose_name='Frame')  # Field name made lowercase.
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
    startoperatorid = models.ForeignKey('WinchOperator', models.DO_NOTHING, db_column='StartOperatorId', null=True, related_name='startoperatorid', verbose_name="Start operator", limit_choices_to={'status': True})  # Field name made lowercase.
    endoperatorid = models.ForeignKey('WinchOperator', models.DO_NOTHING, db_column='EndOperatorId', null=True, related_name='endoperatorid', verbose_name='End operator', limit_choices_to={'status': True})  # Field name made lowercase.
    startdate = models.DateTimeField(db_column='StartDate', null=True, verbose_name='Start date and time')  # Field name made lowercase.
    enddate = models.DateTimeField(db_column='EndDate', blank=True, null=True, verbose_name='End date and time')  # Field name made lowercase.
    deploymenttypeid = models.ForeignKey('Deploymenttype', models.DO_NOTHING, db_column='DeploymentTypeId', null=True, verbose_name='Deployment type', limit_choices_to={'status': True})  # Field name made lowercase.
    wireid = models.ForeignKey('Wire', models.DO_NOTHING, db_column='WireId', blank=True, null=True, verbose_name='Wire')  # Field name made lowercase.
    winchid = models.ForeignKey('Winch', models.DO_NOTHING, db_column='WinchId', null=True, verbose_name='Winch', limit_choices_to={'status': True})  # Field name made lowercase.
    notes = models.TextField(db_column='Notes', blank=True, null=True, verbose_name='Notes')  # Field name made lowercase.
    maxtension = models.IntegerField(db_column='MaxTension', blank=True, null=True, verbose_name='Max tension')  # Field name made lowercase.
    maxpayout = models.IntegerField(db_column='MaxPayout', blank=True, null=True, verbose_name='Max payout')  # Field name made lowercase.
    factorofsafety = models.FloatField(db_column='FactorofSafety', blank=True, null=True, verbose_name='Factor of safety')  # Field name made lowercase.
    flagforreview = models.BooleanField(db_column='Flagforreview', blank=True, null=True, verbose_name='Flag for review')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Cast'
        verbose_name_plural = "Cast"

    def get_absolute_url(self):
        return reverse('castdetail', kwargs={'pk':self.pk})

    def __str__(self):
        return str(self.startdate)

class CutbackRetermination(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    dryendtag = models.IntegerField(db_column='DryEndTag', blank=True, null=True, verbose_name='Dry end tag value (m)')  # Field name made lowercase.
    wetendtag = models.IntegerField(db_column='WetEndTag', blank=True, null=True, verbose_name='Wet end tag value (m)')  # Field name made lowercase.
    lengthremoved = models.IntegerField(db_column='LengthRemoved', blank=True, null=True, verbose_name='Length removed (m)')  # Field name made lowercase.
    wireid = models.ForeignKey('Wire', models.DO_NOTHING, db_column='WireId', blank=True, null=True, verbose_name='Wire')  # Field name made lowercase.
    notes = models.TextField(db_column='Notes', blank=True, null=True, verbose_name='Notes')  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=True, null=True, verbose_name='Date and time')  # Field name made lowercase.
    length = models.TextField(db_column='Length', blank=True, null=True, verbose_name='Length')  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = True
        db_table = 'CutbackRetermination'
        verbose_name_plural = "CutbackRetermination"

    def __str__(self):
        return str(self.date)


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

class Drum(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    internalid = models.TextField(db_column='InternalId', blank=True, null=True, verbose_name='Internal id')  # Field name made lowercase.
    #internalid = models.TextField(db_column='InternalId', blank=True, null=True, verbose_name='Internal id')  # Field name made lowercase.
    color = models.TextField(db_column='Color', blank=True, null=True, verbose_name='Color')  # Field name made lowercase.
    size = models.TextField(db_column='Size', blank=True, null=True, verbose_name='Size')  # Field name made lowercase.
    weight = models.TextField(db_column='Weight', blank=True, null=True, verbose_name='Weight')  # Field name made lowercase.
    material = models.TextField(db_column='Material', blank=True, null=True, verbose_name='Material')  # Field name made lowercase.
    wiretype = models.TextField(db_column='WireType', blank=True, null=True, verbose_name='Wire type')  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = True
        db_table = 'Drum'
        verbose_name_plural = "Drum"

    def __str__(self):
        return str(self.internalid)

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


class Location(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    location = models.TextField(db_column='Location', blank=True, null=True, verbose_name='Location')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Location'
        verbose_name_plural = "Location"

    def __str__(self):
        return str(self.location)

class Lubrication(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    wireid = models.ForeignKey('Wire', models.DO_NOTHING, db_column='WireId', blank=True, null=True, verbose_name='Wire')  # Field name made lowercase.
    lubetype = models.TextField(db_column='LubeType', blank=True, null=True, verbose_name='Lube type')  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=True, null=True, verbose_name='Date and time')  # Field name made lowercase.
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
    #wireid = models.ForeignKey('Wire', models.DO_NOTHING, db_column='WireId', blank=True, null=True, related_name='factorofsafety', verbose_name='Wire')  # Field name made lowercase.
    factorofsafety = models.FloatField(db_column='FactorofSafety', blank=False, null=False, default=5.0, verbose_name='Factor of safety')  # Field name made lowercase.
    #datetime = models.DateTimeField(db_column='DateTime', blank=True, null=True, verbose_name='Date and time')  # Field name made lowercase.
    #enteredby = models.ForeignKey(User, models.DO_NOTHING, db_column='EnteredBy', blank=True, null=True, verbose_name='Entered by')  # Field name made lowercase.
    #notes = models.TextField(db_column='Notes', blank=True, null=True, verbose_name='Notes')  # Field name made lowercase.

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
    datetime = models.DateTimeField(db_column='DateTime', blank=True, null=True, verbose_name='Date and time')  # Field name made lowercase.
    enteredby = models.ForeignKey(User, models.DO_NOTHING, db_column='EnteredBy', blank=True, null=True, verbose_name='Entered by')  # Field name made lowercase.
    drumid = models.ForeignKey(Drum, models.DO_NOTHING, db_column='DrumId', blank=True, null=True, verbose_name='Drum')  # Field name made lowercase.
    winchid = models.ForeignKey(Winch, models.DO_NOTHING, db_column='WinchId', blank=True, null=True, verbose_name='Winch')  # Field name made lowercase.
    locationid = models.ForeignKey(Location, models.DO_NOTHING, db_column='LocationId', blank=True, null=True, verbose_name='Location')  # Field name made lowercase.
    notes = models.TextField(db_column='Notes', blank=True, null=True, verbose_name='notes')  # Field name made lowercase.
    
    class Meta:
        managed = True
        db_table = 'DrumLocation'
        verbose_name_plural = "DrumLocation"
        
    def __str__(self):
        return str(self.locationid) + '-' + str(self.drumid)

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
    wireropeid = models.ForeignKey(WireRopeData, models.DO_NOTHING, db_column='WireRopeId', blank=True, null=True, verbose_name='Wire rope data id')  # Field name made lowercase.
    winchid = models.ForeignKey(Winch, models.DO_NOTHING, db_column='WinchId', blank=True, null=True, verbose_name='Winch')  # Field name made lowercase.
    manufacturerid = models.TextField(db_column='ManufacturerId', blank=True, null=True, verbose_name='Manufacturer id')  # Field name made lowercase.
    nsfid = models.TextField(db_column='NsfId', blank=True, null=True, verbose_name='NSF id')  # Field name made lowercase.
    dateacquired = models.DateTimeField(db_column='DateAcquired', blank=True, null=True, verbose_name='Date Acquired')  # Field name made lowercase.
    #totalbreakingload = models.IntegerField(db_column='TotalBreakingLoad', blank=True, null=True)  # Field name made lowercase.
    notes = models.TextField(db_column='Notes', blank=True, null=True, verbose_name='notes')  # Field name made lowercase.
    length = models.IntegerField(db_column='Length', blank=True, null=True, verbose_name='Length')  # Field name made lowercase.
    status = models.BooleanField(db_column='Status', blank=True, null=True, verbose_name='Status')
    drums = models.ManyToManyField(Drum, through='WireDrum', related_name='loaded_wires', verbose_name='Drum')
    factorofsafety = models.ForeignKey(FactorOfSafety, models.DO_NOTHING, db_column='FactorofSafety', blank=True, null=True, related_name='wirefactorofsafety', verbose_name='Factor of safety')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Wire'
        verbose_name_plural = "Wire"

    def get_absolute_url(self):
        return reverse('wiredetail', kwargs={'pk':self.pk})

    def __str__(self):
        return str(self.nsfid)

    @property
    def nbl(self):
        wireropeidref=Wire.wireropeid.get_object(self)
        nbl=wireropeidref.nominalbreakingload
        return nbl

    @property
    def drum(self):
        d=self.drums.get()
        return d

class Wiredrum(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    drumid = models.ForeignKey(Drum, models.DO_NOTHING, db_column='DrumId', blank=True, null=True, verbose_name='Drum')  # Field name made lowercase.
    wireid = models.ForeignKey(Wire, models.DO_NOTHING, db_column='WireId', blank=True, null=True, verbose_name='Wire')  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=True, null=True, verbose_name='Date and time')  # Field name made lowercase.
    notes = models.TextField(db_column='Notes', blank=True, null=True, verbose_name='Notes')  # Field name made lowercase.
    

    class Meta:
        managed = True
        db_table = 'WireDrum'
        verbose_name_plural = "WireDrum"

    def __str__(self):
        return str(self.drumid)



from django.db import models
from django.urls import reverse


class Calibration(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    appliedloadlow = models.IntegerField(db_column='AppliedLoadLow', blank=True, null=True)  # Field name made lowercase.
    tensionlow = models.IntegerField(db_column='TensionLow', blank=True, null=True)  # Field name made lowercase.
    rawmvlow = models.FloatField(db_column='RawmVLow', blank=True, null=True)  # Field name made lowercase.
    appliedloadhigh = models.IntegerField(db_column='AppliedLoadHigh', blank=True, null=True)  # Field name made lowercase.
    tensionhigh = models.IntegerField(db_column='TensionHigh', blank=True, null=True)  # Field name made lowercase.
    rawmvhigh = models.FloatField(db_column='RawmVHigh', blank=True, null=True)  # Field name made lowercase.
    calibrationid = models.ForeignKey('CalibrationMeta', models.DO_NOTHING, db_column='CalibrationId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Calibration'
        verbose_name_plural = "Calibration"


class CalibrationMeta(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    winchid = models.ForeignKey('Winch', models.DO_NOTHING, db_column='WinchId', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    operatorid = models.ForeignKey('Winchoperator', models.DO_NOTHING, db_column='OperatorId', blank=True, null=True)  # Field name made lowercase.
    wireid = models.ForeignKey('Wire', models.DO_NOTHING, db_column='WireId', blank=True, null=True)  # Field name made lowercase.
    dynomometerid = models.ForeignKey('Dynomometer', models.DO_NOTHING, db_column='DynomometerId', blank=True, null=True)  # Field name made lowercase.
    frameid = models.ForeignKey('Frame', models.DO_NOTHING, db_column='FrameId', blank=True, null=True)  # Field name made lowercase.
    safetyfactor = models.IntegerField(db_column='SafetyFactor', blank=True, null=True)  # Field name made lowercase.
    monitoringaccuracy = models.IntegerField(db_column='MonitoringAccuracy', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'CalibrationMeta'
        verbose_name_plural = "CalibrationMeta"

    def __str__(self):
        return str(self.date)


class Cast(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    startoperatorid = models.ForeignKey('WinchOperator', models.DO_NOTHING, db_column='StartOperatorId', null=True, related_name='startoperatorid')  # Field name made lowercase.
    endoperatorid = models.ForeignKey('WinchOperator', models.DO_NOTHING, db_column='EndOperatorId', null=True, related_name='endoperatorid')  # Field name made lowercase.
    startdate = models.DateTimeField(db_column='StartDate', null=True)  # Field name made lowercase.
    enddate = models.DateTimeField(db_column='EndDate', blank=True, null=True)  # Field name made lowercase.
    deploymenttypeid = models.ForeignKey('Deploymenttype', models.DO_NOTHING, db_column='DeploymentTypeId', null=True)  # Field name made lowercase.
    wireid = models.ForeignKey('Wire', models.DO_NOTHING, db_column='WireId', blank=True, null=True)  # Field name made lowercase.
    winchid = models.ForeignKey('Winch', models.DO_NOTHING, db_column='WinchId', null=True)  # Field name made lowercase.
    notes = models.TextField(db_column='Notes', blank=True, null=True)  # Field name made lowercase.
    maxtension = models.IntegerField(db_column='MaxTension', blank=True, null=True)  # Field name made lowercase.
    maxpayout = models.IntegerField(db_column='MaxPayout', blank=True, null=True)  # Field name made lowercase.

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
    dryendtag = models.IntegerField(db_column='DryEndTag', blank=True, null=True)  # Field name made lowercase.
    wetendtag = models.IntegerField(db_column='WetEndTag', blank=True, null=True)  # Field name made lowercase.
    lengthremoved = models.IntegerField(db_column='LengthRemoved', blank=True, null=True)  # Field name made lowercase.
    wireid = models.ForeignKey('Wire', models.DO_NOTHING, db_column='WireId', blank=True, null=True)  # Field name made lowercase.
    notes = models.TextField(db_column='Notes', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    length = models.TextField(db_column='Length', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    terminationid = models.ForeignKey('Termination', models.DO_NOTHING, db_column='TerminationId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'CutbackRetermination'
        verbose_name_plural = "CutbackRetermination"

    def __str__(self):
        return str(self.date)


class DeploymentType(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    status = models.BooleanField(db_column='Status', blank=True, null=True)  # Field name made lowercase.
    name = models.TextField(db_column='Name', blank=True, null=True)
    equipment = models.TextField(db_column='Equipment', blank=True, null=True)  # Field name made lowercase.
    notes = models.TextField(db_column='Notes', blank=True, null=True)  # Field name made lowercase.

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
    internalid = models.TextField(db_column='InternalId', blank=True, null=True)  # Field name made lowercase.
    color = models.TextField(db_column='Color', blank=True, null=True)  # Field name made lowercase.
    size = models.TextField(db_column='Size', blank=True, null=True)  # Field name made lowercase.
    weight = models.TextField(db_column='Weight', blank=True, null=True)  # Field name made lowercase.
    material = models.TextField(db_column='Material', blank=True, null=True)  # Field name made lowercase.
    wiretype = models.TextField(db_column='WireType', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    locationid = models.ForeignKey('Location', models.DO_NOTHING, db_column='LocationId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Drum'
        verbose_name_plural = "Drum"

    def __str__(self):
        return str(self.internalid)

class Dynomometer(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    name = models.TextField(db_column='Name', blank=True, null=True)  # Field name made lowercase.
    dynomometertype = models.TextField(db_column='DynomometerType', blank=True, null=True)  # Field name made lowercase.
    comments = models.TextField(db_column='Comments', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Dynomometer'
        verbose_name_plural = "Dynomometer"

    def __str__(self):
        return str(self.name)

class Frame(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    name = models.TextField(db_column='Name', blank=True, null=True)  # Field name made lowercase.
    frametype = models.TextField(db_column='FrameType', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Frame'
        verbose_name_plural = "Frame"

    def __str__(self):
        return str(self.name)


class Location(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    location = models.TextField(db_column='Location', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Location'
        verbose_name_plural = "Location"

    def __str__(self):
        return str(self.location)

class Lubrication(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    wireid = models.ForeignKey('Wire', models.DO_NOTHING, db_column='WireId', blank=True, null=True)  # Field name made lowercase.
    lubetype = models.TextField(db_column='LubeType', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    lubelength = models.IntegerField(db_column='LubeLength', blank=True, null=True)  # Field name made lowercase.
    notes = models.TextField(db_column='Notes', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Lubrication'
        verbose_name_plural = "Lubrication"

    def __str__(self):
        return str(self.date)

class Safeworkinglimit(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    wireid = models.ForeignKey('Wire', models.DO_NOTHING, db_column='WireId', blank=True, null=True)  # Field name made lowercase.
    factorofsafety = models.IntegerField(db_column='FactorofSafety', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'SafeWorkingLimit'
        verbose_name_plural = "SafeWorkingLimit"


class Termination(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    name = models.TextField(db_column='TerminationId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Termination'
        verbose_name_plural = "Termination"

    def __str__(self):
        return str(self.name)

class Winch(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    name = models.TextField(db_column='Name', blank=True, null=True)
    locationid = models.ForeignKey(Location, models.DO_NOTHING, db_column='LocationId', blank=True, null=True)  # Field name made lowercase.
    ship = models.TextField(db_column='Ship', blank=True, null=True)  # Field name made lowercase.
    institution = models.TextField(db_column='Institution', blank=True, null=True)  # Field name made lowercase.
    manufacturer = models.TextField(db_column='Manufacturer', blank=True, null=True)  # Field name made lowercase.
    wiretrainschematicjframe = models.TextField(db_column='WireTrainSchematicJFrame', blank=True, null=True)  # Field name made lowercase.
    wiretrainschematicaframe = models.TextField(db_column='WireTrainSchematicAFrame', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Winch'
        verbose_name_plural = "Winch"

    def get_absolute_url(self):
        return reverse('winchdetail', kwargs={'pk':self.pk})

    def __str__(self):
        return str(self.name)

class WinchOperator(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase. This field type is a guess.
    status = models.BooleanField(db_column='Status', blank=True, null=True)  # Field name made lowercase.
    firstname = models.TextField(db_column='FirstName', blank=True, null=True)  # Field name made lowercase.
    lastname = models.TextField(db_column='LastName', blank=True, null=True)  # Field name made lowercase.
    username = models.TextField(db_column='UserName', blank=True, null=True)  # Field name made lowercase.


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
    name = models.TextField(db_column='Name', blank=True, null=True)
    manufacturer = models.TextField(db_column='Manufacturer',blank=True, null=True)
    manufacturerpartnumber = models.TextField(db_column='ManufacturerPartNumber', blank=True, null=True)  # Field name made lowercase.
    cabletype = models.TextField(db_column='CableType', blank=True, null=True)  # Field name made lowercase.
    nominalbreakingload = models.IntegerField(db_column='nominalbreakingload', blank=True, null=True)  # Field name made lowercase.
    weightperfoot = models.FloatField(db_column='WeightPerFoot', blank=True, null=True)  # Field name made lowercase.
    
    class Meta:
        managed = True
        db_table = 'WireRopeData'
        verbose_name_plural = 'WireRopeData'

    def __str__(self):
        return str(self.name)

class Wire(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    wireropeid = models.ForeignKey(WireRopeData, models.DO_NOTHING, db_column='WireRopeId', blank=True, null=True)  # Field name made lowercase.
    manufacturerid = models.TextField(db_column='ManufacturerId', blank=True, null=True)  # Field name made lowercase.
    nsfid = models.TextField(db_column='NsfId', blank=True, null=True)  # Field name made lowercase.
    dateacquired = models.DateTimeField(db_column='DateAcquired', blank=True, null=True)  # Field name made lowercase.
    totalbreakingload = models.IntegerField(db_column='TotalBreakingLoad', blank=True, null=True)  # Field name made lowercase.
    notes = models.TextField(db_column='Notes', blank=True, null=True)  # Field name made lowercase.
    length = models.IntegerField(db_column='Length', blank=True, null=True)  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Wire'
        verbose_name_plural = "Wire"

    def get_absolute_url(self):
        return reverse('wiredetail', kwargs={'pk':self.pk})

    def __str__(self):
        return str(self.nsfid)

class Wiredrum(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    drumid = models.ForeignKey(Drum, models.DO_NOTHING, db_column='DrumId', blank=True, null=True)  # Field name made lowercase.
    wireid = models.ForeignKey(Wire, models.DO_NOTHING, db_column='WireId', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    notes = models.TextField(db_column='Notes', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'WireDrum'
        verbose_name_plural = "WireDrum"

    def __str__(self):
        return str(self.drumid)

class Wiretermination(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    wireid = models.ForeignKey(Wire, models.DO_NOTHING, db_column='WireId', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    notes = models.TextField(db_column='Notes', blank=True, null=True)  # Field name made lowercase.
    terminationid = models.ForeignKey(Termination, models.DO_NOTHING, db_column='TerminationId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'WireTermination'
        verbose_name_plural = "WireTermination"


# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Calibration(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    appliedloadlow = models.IntegerField(db_column='AppliedLoadLow', blank=True, null=True)  # Field name made lowercase.
    tensionlow = models.IntegerField(db_column='TensionLow', blank=True, null=True)  # Field name made lowercase.
    rawmvlow = models.FloatField(db_column='RawmVLow', blank=True, null=True)  # Field name made lowercase.
    appliedloadhigh = models.IntegerField(db_column='AppliedLoadHigh', blank=True, null=True)  # Field name made lowercase.
    tensionhigh = models.IntegerField(db_column='TensionHigh', blank=True, null=True)  # Field name made lowercase.
    rawmvhigh = models.FloatField(db_column='RawmVHigh', blank=True, null=True)  # Field name made lowercase.
    calibrationid = models.IntegerField(db_column='CalibrationId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Calibration'


class Calibrationsmetadata(models.Model):
    id = models.AutoField(db_column='CalibrationsId', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    winchid = models.ForeignKey('Winch', models.DO_NOTHING, db_column='WinchId', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    operatorid = models.ForeignKey('Winchoperator', models.DO_NOTHING, db_column='OperatorId', blank=True, null=True)  # Field name made lowercase.
    wireid = models.ForeignKey('Wire', models.DO_NOTHING, db_column='WireId', blank=True, null=True)  # Field name made lowercase.
    dynomometerid = models.ForeignKey('Dynomometer', models.DO_NOTHING, db_column='DynomometerId', blank=True, null=True)  # Field name made lowercase.
    frameid = models.ForeignKey('Frame', models.DO_NOTHING, db_column='FrameId', blank=True, null=True)  # Field name made lowercase.
    safetyfactor = models.IntegerField(db_column='SafetyFactor', blank=True, null=True)  # Field name made lowercase.
    monitoringaccuracy = models.IntegerField(db_column='MonitoringAccuracy', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CalibrationsMetadata'


class Cast(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    operatorid = models.ForeignKey('Winchoperator', models.DO_NOTHING, db_column='OperatorId')  # Field name made lowercase.
    startdate = models.DateField(db_column='StartDate')  # Field name made lowercase.
    enddate = models.DateField(db_column='EndDate', blank=True, null=True)  # Field name made lowercase.
    deploymenttypeid = models.ForeignKey('Deploymenttype', models.DO_NOTHING, db_column='DeploymentTypeId')  # Field name made lowercase.
    wireid = models.ForeignKey('Wire', models.DO_NOTHING, db_column='WireId', blank=True, null=True)  # Field name made lowercase.
    winchid = models.ForeignKey('Winch', models.DO_NOTHING, db_column='WinchId')  # Field name made lowercase.
    notes = models.TextField(db_column='Notes', blank=True, null=True)  # Field name made lowercase.
    maxtension = models.IntegerField(db_column='MaxTension', blank=True, null=True)  # Field name made lowercase.
    maxpayout = models.IntegerField(db_column='MaxPayout', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Cast'


class Cutbacksretermination(models.Model):
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
        managed = False
        db_table = 'CutbacksRetermination'


class Deploymenttype(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    equipment = models.TextField(db_column='Equipment', blank=True, null=True)  # Field name made lowercase.
    notes = models.TextField(db_column='Notes', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DeploymentType'


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
        managed = False
        db_table = 'Drum'


class Dynomometer(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    dynomometertype = models.TextField(db_column='DynomometerType', blank=True, null=True)  # Field name made lowercase.
    comments = models.TextField(db_column='Comments', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dynomometer'


class Frame(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    frametype = models.TextField(db_column='FrameType', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Frame'


class Location(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    location = models.TextField(db_column='Location', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Location'


class Lubrication(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    wireid = models.ForeignKey('Wire', models.DO_NOTHING, db_column='WireId', blank=True, null=True)  # Field name made lowercase.
    lubetype = models.TextField(db_column='LubeType', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    lubelength = models.IntegerField(db_column='LubeLength', blank=True, null=True)  # Field name made lowercase.
    notes = models.TextField(db_column='Notes', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Lubrication'


class Safeworkinglimit(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    wireid = models.ForeignKey('Wire', models.DO_NOTHING, db_column='WireId', blank=True, null=True)  # Field name made lowercase.
    freeendsafetyfactor = models.IntegerField(db_column='FreeEndSafetyFactor', blank=True, null=True)  # Field name made lowercase.
    fixedendsafetyfactor = models.IntegerField(db_column='FixedEndSafetyFactor', blank=True, null=True)  # Field name made lowercase.
    freeendsafeworkingload = models.IntegerField(db_column='FreeEndSafeWorkingLoad', blank=True, null=True)  # Field name made lowercase.
    fixedendsafeworkingload = models.IntegerField(db_column='FixedEndSafeWorkingLoad', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SafeWorkingLimit'


class Termination(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    terminationid = models.TextField(db_column='TerminationId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Termination'


class Winch(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    locationid = models.ForeignKey(Location, models.DO_NOTHING, db_column='LocationId', blank=True, null=True)  # Field name made lowercase.
    ship = models.TextField(db_column='Ship', blank=True, null=True)  # Field name made lowercase.
    institution = models.TextField(db_column='Institution', blank=True, null=True)  # Field name made lowercase.
    manufacturer = models.TextField(db_column='Manufacturer', blank=True, null=True)  # Field name made lowercase.
    wiretrainschematicjframe = models.TextField(db_column='WireTrainSchematicJFrame', blank=True, null=True)  # Field name made lowercase.
    wiretrainschematicaframe = models.TextField(db_column='WireTrainSchematicAFrame', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Winch'


class Winchoperator(models.Model):
    id = models.TextField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase. This field type is a guess.
    status = models.BooleanField(db_column='Status', blank=True, null=True)  # Field name made lowercase.
    firstname = models.TextField(db_column='FirstName', blank=True, null=True)  # Field name made lowercase.
    lastname = models.TextField(db_column='LastName', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'WinchOperator'


class Wire(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    manufacturerid = models.TextField(db_column='ManufacturerId', blank=True, null=True)  # Field name made lowercase.
    nsfid = models.TextField(db_column='NsfId', blank=True, null=True)  # Field name made lowercase.
    manufacturerpartnumber = models.TextField(db_column='ManufacturerPartNumber', blank=True, null=True)  # Field name made lowercase.
    manufacturer = models.TextField(db_column='Manufacturer', blank=True, null=True)  # Field name made lowercase.
    cabletype = models.TextField(db_column='CableType', blank=True, null=True)  # Field name made lowercase.
    dateacquired = models.DateTimeField(db_column='DateAcquired', blank=True, null=True)  # Field name made lowercase.
    totalbreakingload = models.IntegerField(db_column='TotalBreakingLoad', blank=True, null=True)  # Field name made lowercase.
    notes = models.TextField(db_column='Notes', blank=True, null=True)  # Field name made lowercase.
    nominalbreakingload = models.IntegerField(db_column='NominalBreakingLoad', blank=True, null=True)  # Field name made lowercase.
    length = models.IntegerField(db_column='Length', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Wire'


class Wiredrum(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    drumid = models.ForeignKey(Drum, models.DO_NOTHING, db_column='DrumId', blank=True, null=True)  # Field name made lowercase.
    wireid = models.ForeignKey(Wire, models.DO_NOTHING, db_column='WireId', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    notes = models.TextField(db_column='Notes', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'WireDrum'


class Wiretermination(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    wireid = models.ForeignKey(Wire, models.DO_NOTHING, db_column='WireId', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    notes = models.TextField(db_column='Notes', blank=True, null=True)  # Field name made lowercase.
    terminationid = models.ForeignKey(Termination, models.DO_NOTHING, db_column='TerminationId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'WireTermination'

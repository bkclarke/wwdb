# Generated by Django 4.1.3 on 2022-12-07 14:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("wwdb", "0023_remove_drum_wire_alter_cast_startoperatorid"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="factorofsafety",
            name="wireid",
        ),
        migrations.RemoveField(
            model_name="wire",
            name="totalbreakingload",
        ),
        migrations.AddField(
            model_name="wire",
            name="factorofsafety",
            field=models.ForeignKey(
                blank=True,
                db_column="FactorofSafety",
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="wirefactorofsafety",
                to="wwdb.factorofsafety",
                verbose_name="Factor of safety",
            ),
        ),
        migrations.AlterField(
            model_name="breaktest",
            name="notes",
            field=models.TextField(
                blank=True, db_column="Notes", null=True, verbose_name="Notes"
            ),
        ),
        migrations.AlterField(
            model_name="breaktest",
            name="testdate",
            field=models.DateTimeField(
                blank=True, db_column="TestDate", null=True, verbose_name="Test date"
            ),
        ),
        migrations.AlterField(
            model_name="breaktest",
            name="testedbreakingload",
            field=models.IntegerField(
                blank=True,
                db_column="TestedBreakingLoad",
                null=True,
                verbose_name="Tested breaking load",
            ),
        ),
        migrations.AlterField(
            model_name="breaktest",
            name="wireid",
            field=models.ForeignKey(
                blank=True,
                db_column="WireId",
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="wwdb.wire",
                verbose_name="Wire",
            ),
        ),
        migrations.AlterField(
            model_name="calibration",
            name="appliedloadhigh",
            field=models.IntegerField(
                blank=True,
                db_column="AppliedLoadHigh",
                null=True,
                verbose_name="Highest applied load",
            ),
        ),
        migrations.AlterField(
            model_name="calibration",
            name="appliedloadlow",
            field=models.IntegerField(
                blank=True,
                db_column="AppliedLoadLow",
                null=True,
                verbose_name="Lowest applied load",
            ),
        ),
        migrations.AlterField(
            model_name="calibration",
            name="calibrationid",
            field=models.ForeignKey(
                blank=True,
                db_column="CalibrationId",
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="wwdb.calibrationmeta",
                verbose_name="Calibration id",
            ),
        ),
        migrations.AlterField(
            model_name="calibration",
            name="rawmvhigh",
            field=models.FloatField(
                blank=True,
                db_column="RawmVHigh",
                null=True,
                verbose_name="Highest raw mv",
            ),
        ),
        migrations.AlterField(
            model_name="calibration",
            name="rawmvlow",
            field=models.FloatField(
                blank=True,
                db_column="RawmVLow",
                null=True,
                verbose_name="Lowest raw mv",
            ),
        ),
        migrations.AlterField(
            model_name="calibration",
            name="tensionhigh",
            field=models.IntegerField(
                blank=True,
                db_column="TensionHigh",
                null=True,
                verbose_name="Highest tension",
            ),
        ),
        migrations.AlterField(
            model_name="calibration",
            name="tensionlow",
            field=models.IntegerField(
                blank=True,
                db_column="TensionLow",
                null=True,
                verbose_name="Lowest tension",
            ),
        ),
        migrations.AlterField(
            model_name="calibrationmeta",
            name="date",
            field=models.DateField(
                blank=True, db_column="Date", null=True, verbose_name="Date"
            ),
        ),
        migrations.AlterField(
            model_name="calibrationmeta",
            name="dynomometerid",
            field=models.ForeignKey(
                blank=True,
                db_column="DynomometerId",
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="wwdb.dynomometer",
                verbose_name="Dynomometer",
            ),
        ),
        migrations.AlterField(
            model_name="calibrationmeta",
            name="frameid",
            field=models.ForeignKey(
                blank=True,
                db_column="FrameId",
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="wwdb.frame",
                verbose_name="Frame",
            ),
        ),
        migrations.AlterField(
            model_name="calibrationmeta",
            name="monitoringaccuracy",
            field=models.IntegerField(
                blank=True,
                db_column="MonitoringAccuracy",
                null=True,
                verbose_name="Monitoring accuracy",
            ),
        ),
        migrations.AlterField(
            model_name="calibrationmeta",
            name="operatorid",
            field=models.ForeignKey(
                blank=True,
                db_column="OperatorId",
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="wwdb.winchoperator",
                verbose_name="Operator",
            ),
        ),
        migrations.AlterField(
            model_name="calibrationmeta",
            name="safetyfactor",
            field=models.IntegerField(
                blank=True,
                db_column="SafetyFactor",
                null=True,
                verbose_name="Factor of safety",
            ),
        ),
        migrations.AlterField(
            model_name="calibrationmeta",
            name="winchid",
            field=models.ForeignKey(
                blank=True,
                db_column="WinchId",
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="wwdb.winch",
                verbose_name="Winch",
            ),
        ),
        migrations.AlterField(
            model_name="calibrationmeta",
            name="wireid",
            field=models.ForeignKey(
                blank=True,
                db_column="WireId",
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="wwdb.wire",
                verbose_name="Wire id",
            ),
        ),
        migrations.AlterField(
            model_name="cast",
            name="deploymenttypeid",
            field=models.ForeignKey(
                db_column="DeploymentTypeId",
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="wwdb.deploymenttype",
                verbose_name="Deployment type",
            ),
        ),
        migrations.AlterField(
            model_name="cast",
            name="enddate",
            field=models.DateTimeField(
                blank=True,
                db_column="EndDate",
                null=True,
                verbose_name="End date and time",
            ),
        ),
        migrations.AlterField(
            model_name="cast",
            name="endoperatorid",
            field=models.ForeignKey(
                db_column="EndOperatorId",
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="endoperatorid",
                to="wwdb.winchoperator",
                verbose_name="End operator",
            ),
        ),
        migrations.AlterField(
            model_name="cast",
            name="maxpayout",
            field=models.IntegerField(
                blank=True, db_column="MaxPayout", null=True, verbose_name="Max payout"
            ),
        ),
        migrations.AlterField(
            model_name="cast",
            name="maxtension",
            field=models.IntegerField(
                blank=True,
                db_column="MaxTension",
                null=True,
                verbose_name="Max tension",
            ),
        ),
        migrations.AlterField(
            model_name="cast",
            name="notes",
            field=models.TextField(
                blank=True, db_column="Notes", null=True, verbose_name="Notes"
            ),
        ),
        migrations.AlterField(
            model_name="cast",
            name="startdate",
            field=models.DateTimeField(
                db_column="StartDate", null=True, verbose_name="Start date and time"
            ),
        ),
        migrations.AlterField(
            model_name="cast",
            name="winchid",
            field=models.ForeignKey(
                db_column="WinchId",
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="wwdb.winch",
                verbose_name="Winch",
            ),
        ),
        migrations.AlterField(
            model_name="cast",
            name="wireid",
            field=models.ForeignKey(
                blank=True,
                db_column="WireId",
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="wwdb.wire",
                verbose_name="Wire",
            ),
        ),
        migrations.AlterField(
            model_name="cutbackretermination",
            name="date",
            field=models.DateField(
                blank=True, db_column="Date", null=True, verbose_name="Date and time"
            ),
        ),
        migrations.AlterField(
            model_name="cutbackretermination",
            name="dryendtag",
            field=models.IntegerField(
                blank=True,
                db_column="DryEndTag",
                null=True,
                verbose_name="Dry end tag value (m)",
            ),
        ),
        migrations.AlterField(
            model_name="cutbackretermination",
            name="length",
            field=models.TextField(
                blank=True, db_column="Length", null=True, verbose_name="Length"
            ),
        ),
        migrations.AlterField(
            model_name="cutbackretermination",
            name="lengthremoved",
            field=models.IntegerField(
                blank=True,
                db_column="LengthRemoved",
                null=True,
                verbose_name="Length removed (m)",
            ),
        ),
        migrations.AlterField(
            model_name="cutbackretermination",
            name="notes",
            field=models.TextField(
                blank=True, db_column="Notes", null=True, verbose_name="Notes"
            ),
        ),
        migrations.AlterField(
            model_name="cutbackretermination",
            name="wetendtag",
            field=models.IntegerField(
                blank=True,
                db_column="WetEndTag",
                null=True,
                verbose_name="Wet end tag value (m)",
            ),
        ),
        migrations.AlterField(
            model_name="cutbackretermination",
            name="wireid",
            field=models.ForeignKey(
                blank=True,
                db_column="WireId",
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="wwdb.wire",
                verbose_name="Wire",
            ),
        ),
        migrations.AlterField(
            model_name="deploymenttype",
            name="equipment",
            field=models.TextField(
                blank=True, db_column="Equipment", null=True, verbose_name="Equipment"
            ),
        ),
        migrations.AlterField(
            model_name="deploymenttype",
            name="name",
            field=models.TextField(
                blank=True, db_column="Name", null=True, verbose_name="Name"
            ),
        ),
        migrations.AlterField(
            model_name="deploymenttype",
            name="notes",
            field=models.TextField(
                blank=True, db_column="Notes", null=True, verbose_name="Notes"
            ),
        ),
        migrations.AlterField(
            model_name="deploymenttype",
            name="status",
            field=models.BooleanField(
                blank=True, db_column="Status", null=True, verbose_name="Status"
            ),
        ),
        migrations.AlterField(
            model_name="drum",
            name="color",
            field=models.TextField(
                blank=True, db_column="Color", null=True, verbose_name="Color"
            ),
        ),
        migrations.AlterField(
            model_name="drum",
            name="internalid",
            field=models.TextField(
                blank=True,
                db_column="InternalId",
                null=True,
                verbose_name="Internal id",
            ),
        ),
        migrations.AlterField(
            model_name="drum",
            name="material",
            field=models.TextField(
                blank=True, db_column="Material", null=True, verbose_name="Material"
            ),
        ),
        migrations.AlterField(
            model_name="drum",
            name="size",
            field=models.TextField(
                blank=True, db_column="Size", null=True, verbose_name="Size"
            ),
        ),
        migrations.AlterField(
            model_name="drum",
            name="weight",
            field=models.TextField(
                blank=True, db_column="Weight", null=True, verbose_name="Weight"
            ),
        ),
        migrations.AlterField(
            model_name="drum",
            name="wiretype",
            field=models.TextField(
                blank=True, db_column="WireType", null=True, verbose_name="Wire type"
            ),
        ),
        migrations.AlterField(
            model_name="drumlocation",
            name="datetime",
            field=models.DateTimeField(
                blank=True,
                db_column="DateTime",
                null=True,
                verbose_name="Date and time",
            ),
        ),
        migrations.AlterField(
            model_name="drumlocation",
            name="drumid",
            field=models.ForeignKey(
                blank=True,
                db_column="DrumId",
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="wwdb.drum",
                verbose_name="Drum",
            ),
        ),
        migrations.AlterField(
            model_name="drumlocation",
            name="enteredby",
            field=models.ForeignKey(
                blank=True,
                db_column="EnteredBy",
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Entered by",
            ),
        ),
        migrations.AlterField(
            model_name="drumlocation",
            name="locationid",
            field=models.ForeignKey(
                blank=True,
                db_column="LocationId",
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="wwdb.location",
                verbose_name="Location",
            ),
        ),
        migrations.AlterField(
            model_name="drumlocation",
            name="notes",
            field=models.TextField(
                blank=True, db_column="Notes", null=True, verbose_name="notes"
            ),
        ),
        migrations.AlterField(
            model_name="drumlocation",
            name="winchid",
            field=models.ForeignKey(
                blank=True,
                db_column="WinchId",
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="wwdb.winch",
                verbose_name="Winch",
            ),
        ),
        migrations.AlterField(
            model_name="dynomometer",
            name="comments",
            field=models.TextField(
                blank=True, db_column="Comments", null=True, verbose_name="notes"
            ),
        ),
        migrations.AlterField(
            model_name="dynomometer",
            name="dynomometertype",
            field=models.TextField(
                blank=True,
                db_column="DynomometerType",
                null=True,
                verbose_name="Dynomometer type",
            ),
        ),
        migrations.AlterField(
            model_name="dynomometer",
            name="name",
            field=models.TextField(
                blank=True, db_column="Name", null=True, verbose_name="Name"
            ),
        ),
        migrations.AlterField(
            model_name="factorofsafety",
            name="datetime",
            field=models.DateTimeField(
                blank=True,
                db_column="DateTime",
                null=True,
                verbose_name="Date and time",
            ),
        ),
        migrations.AlterField(
            model_name="factorofsafety",
            name="enteredby",
            field=models.ForeignKey(
                blank=True,
                db_column="EnteredBy",
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Entered by",
            ),
        ),
        migrations.AlterField(
            model_name="factorofsafety",
            name="factorofsafety",
            field=models.FloatField(
                db_column="FactorofSafety", default=5.0, verbose_name="Factor of safety"
            ),
        ),
        migrations.AlterField(
            model_name="factorofsafety",
            name="notes",
            field=models.TextField(
                blank=True, db_column="Notes", null=True, verbose_name="Notes"
            ),
        ),
        migrations.AlterField(
            model_name="frame",
            name="frametype",
            field=models.TextField(
                blank=True, db_column="FrameType", null=True, verbose_name="Frame type"
            ),
        ),
        migrations.AlterField(
            model_name="frame",
            name="name",
            field=models.TextField(
                blank=True, db_column="Name", null=True, verbose_name="Name"
            ),
        ),
        migrations.AlterField(
            model_name="location",
            name="location",
            field=models.TextField(
                blank=True, db_column="Location", null=True, verbose_name="Location"
            ),
        ),
        migrations.AlterField(
            model_name="lubrication",
            name="date",
            field=models.DateField(
                blank=True, db_column="Date", null=True, verbose_name="Date and time"
            ),
        ),
        migrations.AlterField(
            model_name="lubrication",
            name="lubelength",
            field=models.IntegerField(
                blank=True,
                db_column="LubeLength",
                null=True,
                verbose_name="Length lubed",
            ),
        ),
        migrations.AlterField(
            model_name="lubrication",
            name="lubetype",
            field=models.TextField(
                blank=True, db_column="LubeType", null=True, verbose_name="Lube type"
            ),
        ),
        migrations.AlterField(
            model_name="lubrication",
            name="notes",
            field=models.TextField(
                blank=True, db_column="Notes", null=True, verbose_name="Notes"
            ),
        ),
        migrations.AlterField(
            model_name="lubrication",
            name="wireid",
            field=models.ForeignKey(
                blank=True,
                db_column="WireId",
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="wwdb.wire",
                verbose_name="Wire",
            ),
        ),
        migrations.AlterField(
            model_name="winch",
            name="active",
            field=models.BooleanField(
                db_column="Active", default=True, verbose_name="Active = True"
            ),
        ),
        migrations.AlterField(
            model_name="winch",
            name="drums",
            field=models.ManyToManyField(
                related_name="winches",
                through="wwdb.DrumLocation",
                to="wwdb.drum",
                verbose_name="Drum",
            ),
        ),
        migrations.AlterField(
            model_name="winch",
            name="institution",
            field=models.TextField(
                blank=True,
                db_column="Institution",
                null=True,
                verbose_name="Institution",
            ),
        ),
        migrations.AlterField(
            model_name="winch",
            name="manufacturer",
            field=models.TextField(
                blank=True,
                db_column="Manufacturer",
                null=True,
                verbose_name="Manufacturer",
            ),
        ),
        migrations.AlterField(
            model_name="winch",
            name="name",
            field=models.TextField(
                blank=True, db_column="Name", null=True, verbose_name="Name"
            ),
        ),
        migrations.AlterField(
            model_name="winch",
            name="ship",
            field=models.TextField(
                blank=True, db_column="Ship", null=True, verbose_name="Ship"
            ),
        ),
        migrations.AlterField(
            model_name="winch",
            name="wiretrainschematicaframe",
            field=models.TextField(
                blank=True,
                db_column="WireTrainSchematicAFrame",
                null=True,
                verbose_name="Wire train schematic Aframe",
            ),
        ),
        migrations.AlterField(
            model_name="winch",
            name="wiretrainschematicjframe",
            field=models.TextField(
                blank=True,
                db_column="WireTrainSchematicJFrame",
                null=True,
                verbose_name="Wire train schematic Jframe",
            ),
        ),
        migrations.AlterField(
            model_name="winchoperator",
            name="firstname",
            field=models.TextField(
                blank=True, db_column="FirstName", null=True, verbose_name="First name"
            ),
        ),
        migrations.AlterField(
            model_name="winchoperator",
            name="lastname",
            field=models.TextField(
                blank=True, db_column="LastName", null=True, verbose_name="Last name"
            ),
        ),
        migrations.AlterField(
            model_name="winchoperator",
            name="status",
            field=models.BooleanField(
                blank=True, db_column="Status", null=True, verbose_name="Status"
            ),
        ),
        migrations.AlterField(
            model_name="winchoperator",
            name="username",
            field=models.TextField(
                blank=True, db_column="UserName", null=True, verbose_name="User name"
            ),
        ),
        migrations.AlterField(
            model_name="wire",
            name="dateacquired",
            field=models.DateTimeField(
                blank=True,
                db_column="DateAcquired",
                null=True,
                verbose_name="Date Acquired",
            ),
        ),
        migrations.AlterField(
            model_name="wire",
            name="drums",
            field=models.ManyToManyField(
                related_name="loaded_wires",
                through="wwdb.Wiredrum",
                to="wwdb.drum",
                verbose_name="Drum",
            ),
        ),
        migrations.AlterField(
            model_name="wire",
            name="length",
            field=models.IntegerField(
                blank=True, db_column="Length", null=True, verbose_name="Length"
            ),
        ),
        migrations.AlterField(
            model_name="wire",
            name="manufacturerid",
            field=models.TextField(
                blank=True,
                db_column="ManufacturerId",
                null=True,
                verbose_name="Manufacturer id",
            ),
        ),
        migrations.AlterField(
            model_name="wire",
            name="notes",
            field=models.TextField(
                blank=True, db_column="Notes", null=True, verbose_name="notes"
            ),
        ),
        migrations.AlterField(
            model_name="wire",
            name="nsfid",
            field=models.TextField(
                blank=True, db_column="NsfId", null=True, verbose_name="NSF id"
            ),
        ),
        migrations.AlterField(
            model_name="wire",
            name="status",
            field=models.BooleanField(
                blank=True, db_column="Status", null=True, verbose_name="Status"
            ),
        ),
        migrations.AlterField(
            model_name="wire",
            name="winchid",
            field=models.ForeignKey(
                blank=True,
                db_column="WinchId",
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="wwdb.winch",
                verbose_name="Winch",
            ),
        ),
        migrations.AlterField(
            model_name="wire",
            name="wireropeid",
            field=models.ForeignKey(
                blank=True,
                db_column="WireRopeId",
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="wwdb.wireropedata",
                verbose_name="Wire rope data id",
            ),
        ),
        migrations.AlterField(
            model_name="wiredrum",
            name="date",
            field=models.DateField(
                blank=True, db_column="Date", null=True, verbose_name="Date and time"
            ),
        ),
        migrations.AlterField(
            model_name="wiredrum",
            name="drumid",
            field=models.ForeignKey(
                blank=True,
                db_column="DrumId",
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="wwdb.drum",
                verbose_name="Drum",
            ),
        ),
        migrations.AlterField(
            model_name="wiredrum",
            name="notes",
            field=models.TextField(
                blank=True, db_column="Notes", null=True, verbose_name="Notes"
            ),
        ),
        migrations.AlterField(
            model_name="wiredrum",
            name="wireid",
            field=models.ForeignKey(
                blank=True,
                db_column="WireId",
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="wwdb.wire",
                verbose_name="Wire",
            ),
        ),
        migrations.AlterField(
            model_name="wireropedata",
            name="cabletype",
            field=models.TextField(
                blank=True, db_column="CableType", null=True, verbose_name="Cable type"
            ),
        ),
        migrations.AlterField(
            model_name="wireropedata",
            name="manufacturer",
            field=models.TextField(
                blank=True,
                db_column="Manufacturer",
                null=True,
                verbose_name="Manufacturer",
            ),
        ),
        migrations.AlterField(
            model_name="wireropedata",
            name="manufacturerpartnumber",
            field=models.TextField(
                blank=True,
                db_column="ManufacturerPartNumber",
                null=True,
                verbose_name="Manufacturer part number",
            ),
        ),
        migrations.AlterField(
            model_name="wireropedata",
            name="name",
            field=models.TextField(
                blank=True, db_column="Name", null=True, verbose_name="Name"
            ),
        ),
        migrations.AlterField(
            model_name="wireropedata",
            name="nominalbreakingload",
            field=models.IntegerField(
                blank=True,
                db_column="nominalbreakingload",
                null=True,
                verbose_name="Nominal breaking load",
            ),
        ),
        migrations.AlterField(
            model_name="wireropedata",
            name="weightperfoot",
            field=models.FloatField(
                blank=True,
                db_column="WeightPerFoot",
                null=True,
                verbose_name="Weight per foot",
            ),
        ),
    ]
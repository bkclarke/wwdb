# Generated by Django 4.1.3 on 2024-07-09 01:45

from django.db import migrations, models
import wwdb.models


class Migration(migrations.Migration):

    dependencies = [
        ("wwdb", "0076_remove_cruise_status_cruise_winch1status_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="breaktest",
            name="notes",
            field=models.TextField(
                blank=True,
                db_column="Notes",
                null=True,
                validators=[wwdb.models.validate_commas],
                verbose_name="Notes",
            ),
        ),
        migrations.AlterField(
            model_name="cast",
            name="notes",
            field=models.TextField(
                blank=True,
                db_column="Notes",
                null=True,
                validators=[wwdb.models.validate_commas],
                verbose_name="Notes",
            ),
        ),
        migrations.AlterField(
            model_name="cruise",
            name="winch1status",
            field=models.BooleanField(
                blank=True,
                db_column="Winch1Status",
                null=True,
                validators=[wwdb.models.validate_commas],
                verbose_name="Winch 1 status",
            ),
        ),
        migrations.AlterField(
            model_name="cruise",
            name="winch2status",
            field=models.BooleanField(
                blank=True,
                db_column="Winch2Status",
                null=True,
                validators=[wwdb.models.validate_commas],
                verbose_name="Winch 2 status",
            ),
        ),
        migrations.AlterField(
            model_name="cruise",
            name="winch3status",
            field=models.BooleanField(
                blank=True,
                db_column="Winch3Status",
                null=True,
                validators=[wwdb.models.validate_commas],
                verbose_name="Winch 3 status",
            ),
        ),
        migrations.AlterField(
            model_name="deploymenttype",
            name="equipment",
            field=models.TextField(
                blank=True,
                db_column="Equipment",
                null=True,
                validators=[wwdb.models.validate_commas],
                verbose_name="Equipment",
            ),
        ),
        migrations.AlterField(
            model_name="deploymenttype",
            name="name",
            field=models.TextField(
                blank=True,
                db_column="Name",
                null=True,
                validators=[wwdb.models.validate_commas],
                verbose_name="Name",
            ),
        ),
        migrations.AlterField(
            model_name="deploymenttype",
            name="notes",
            field=models.TextField(
                blank=True,
                db_column="Notes",
                null=True,
                validators=[wwdb.models.validate_commas],
                verbose_name="Notes",
            ),
        ),
        migrations.AlterField(
            model_name="drum",
            name="color",
            field=models.TextField(
                blank=True,
                db_column="Color",
                null=True,
                validators=[wwdb.models.validate_commas],
                verbose_name="Color",
            ),
        ),
        migrations.AlterField(
            model_name="drum",
            name="internalid",
            field=models.TextField(
                blank=True,
                db_column="InternalId",
                null=True,
                validators=[wwdb.models.validate_commas],
                verbose_name="Internal id",
            ),
        ),
        migrations.AlterField(
            model_name="drum",
            name="material",
            field=models.TextField(
                blank=True,
                db_column="Material",
                null=True,
                validators=[wwdb.models.validate_commas],
                verbose_name="Material",
            ),
        ),
        migrations.AlterField(
            model_name="drum",
            name="size",
            field=models.TextField(
                blank=True,
                db_column="Size",
                null=True,
                validators=[wwdb.models.validate_commas],
                verbose_name="Size",
            ),
        ),
        migrations.AlterField(
            model_name="drum",
            name="weight",
            field=models.TextField(
                blank=True,
                db_column="Weight",
                null=True,
                validators=[wwdb.models.validate_commas],
                verbose_name="Weight",
            ),
        ),
        migrations.AlterField(
            model_name="drum",
            name="wiretype",
            field=models.TextField(
                blank=True,
                db_column="WireType",
                null=True,
                validators=[wwdb.models.validate_commas],
                verbose_name="Wire type",
            ),
        ),
        migrations.AlterField(
            model_name="drumlocation",
            name="notes",
            field=models.TextField(
                blank=True,
                db_column="Notes",
                null=True,
                validators=[wwdb.models.validate_commas],
                verbose_name="notes",
            ),
        ),
        migrations.AlterField(
            model_name="dynomometer",
            name="comments",
            field=models.TextField(
                blank=True,
                db_column="Comments",
                null=True,
                validators=[wwdb.models.validate_commas],
                verbose_name="notes",
            ),
        ),
        migrations.AlterField(
            model_name="dynomometer",
            name="dynomometertype",
            field=models.TextField(
                blank=True,
                db_column="DynomometerType",
                null=True,
                validators=[wwdb.models.validate_commas],
                verbose_name="Dynomometer type",
            ),
        ),
        migrations.AlterField(
            model_name="dynomometer",
            name="name",
            field=models.TextField(
                blank=True,
                db_column="Name",
                null=True,
                validators=[wwdb.models.validate_commas],
                verbose_name="Name",
            ),
        ),
        migrations.AlterField(
            model_name="frame",
            name="frametype",
            field=models.TextField(
                blank=True,
                db_column="FrameType",
                null=True,
                validators=[wwdb.models.validate_commas],
                verbose_name="Frame type",
            ),
        ),
        migrations.AlterField(
            model_name="frame",
            name="name",
            field=models.TextField(
                blank=True,
                db_column="Name",
                null=True,
                validators=[wwdb.models.validate_commas],
                verbose_name="Name",
            ),
        ),
        migrations.AlterField(
            model_name="location",
            name="location",
            field=models.TextField(
                blank=True,
                db_column="Location",
                null=True,
                validators=[wwdb.models.validate_commas],
                verbose_name="Location",
            ),
        ),
        migrations.AlterField(
            model_name="lubrication",
            name="lubetype",
            field=models.TextField(
                blank=True,
                db_column="LubeType",
                null=True,
                validators=[wwdb.models.validate_commas],
                verbose_name="Lube type",
            ),
        ),
        migrations.AlterField(
            model_name="lubrication",
            name="notes",
            field=models.TextField(
                blank=True,
                db_column="Notes",
                null=True,
                validators=[wwdb.models.validate_commas],
                verbose_name="Notes",
            ),
        ),
        migrations.AlterField(
            model_name="winch",
            name="institution",
            field=models.TextField(
                blank=True,
                db_column="Institution",
                null=True,
                validators=[wwdb.models.validate_commas],
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
                validators=[wwdb.models.validate_commas],
                verbose_name="Manufacturer",
            ),
        ),
        migrations.AlterField(
            model_name="winch",
            name="name",
            field=models.TextField(
                blank=True,
                db_column="Name",
                null=True,
                validators=[wwdb.models.validate_commas],
                verbose_name="Name",
            ),
        ),
        migrations.AlterField(
            model_name="winch",
            name="ship",
            field=models.TextField(
                blank=True,
                db_column="Ship",
                null=True,
                validators=[wwdb.models.validate_commas],
                verbose_name="Ship",
            ),
        ),
        migrations.AlterField(
            model_name="winch",
            name="wiretrainschematicaframe",
            field=models.TextField(
                blank=True,
                db_column="WireTrainSchematicAFrame",
                null=True,
                validators=[wwdb.models.validate_commas],
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
                validators=[wwdb.models.validate_commas],
                verbose_name="Wire train schematic Jframe",
            ),
        ),
        migrations.AlterField(
            model_name="winchoperator",
            name="firstname",
            field=models.TextField(
                blank=True,
                db_column="FirstName",
                null=True,
                validators=[wwdb.models.validate_commas],
                verbose_name="First name",
            ),
        ),
        migrations.AlterField(
            model_name="winchoperator",
            name="lastname",
            field=models.TextField(
                blank=True,
                db_column="LastName",
                null=True,
                validators=[wwdb.models.validate_commas],
                verbose_name="Last name",
            ),
        ),
        migrations.AlterField(
            model_name="winchoperator",
            name="username",
            field=models.TextField(
                blank=True,
                db_column="UserName",
                null=True,
                validators=[wwdb.models.validate_commas],
                verbose_name="User name",
            ),
        ),
        migrations.AlterField(
            model_name="wire",
            name="manufacturerid",
            field=models.TextField(
                blank=True,
                db_column="ManufacturerId",
                null=True,
                validators=[wwdb.models.validate_commas],
                verbose_name="Manufacturer id",
            ),
        ),
        migrations.AlterField(
            model_name="wire",
            name="notes",
            field=models.TextField(
                blank=True,
                db_column="Notes",
                null=True,
                validators=[wwdb.models.validate_commas],
                verbose_name="notes",
            ),
        ),
        migrations.AlterField(
            model_name="wire",
            name="nsfid",
            field=models.TextField(
                blank=True,
                db_column="NsfId",
                null=True,
                validators=[wwdb.models.validate_commas],
                verbose_name="NSF id",
            ),
        ),
        migrations.AlterField(
            model_name="wiredrum",
            name="notes",
            field=models.TextField(
                blank=True,
                db_column="Notes",
                null=True,
                validators=[wwdb.models.validate_commas],
                verbose_name="Notes",
            ),
        ),
        migrations.AlterField(
            model_name="wireropedata",
            name="cabletype",
            field=models.TextField(
                blank=True,
                db_column="CableType",
                null=True,
                validators=[wwdb.models.validate_commas],
                verbose_name="Cable type",
            ),
        ),
        migrations.AlterField(
            model_name="wireropedata",
            name="manufacturer",
            field=models.TextField(
                blank=True,
                db_column="Manufacturer",
                null=True,
                validators=[wwdb.models.validate_commas],
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
                validators=[wwdb.models.validate_commas],
                verbose_name="Manufacturer part number",
            ),
        ),
        migrations.AlterField(
            model_name="wireropedata",
            name="name",
            field=models.TextField(
                blank=True,
                db_column="Name",
                null=True,
                validators=[wwdb.models.validate_commas],
                verbose_name="Name",
            ),
        ),
    ]
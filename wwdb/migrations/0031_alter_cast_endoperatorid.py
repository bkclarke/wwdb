# Generated by Django 4.1.3 on 2022-12-09 12:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("wwdb", "0030_alter_cast_factorofsafety"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cast",
            name="endoperatorid",
            field=models.ForeignKey(
                db_column="EndOperatorId",
                limit_choices_to={"status": True},
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="endoperatorid",
                to="wwdb.winchoperator",
                verbose_name="End operator",
            ),
        ),
    ]
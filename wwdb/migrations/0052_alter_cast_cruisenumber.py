# Generated by Django 4.1.3 on 2023-01-15 23:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("wwdb", "0051_alter_cast_cruisenumber"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cast",
            name="cruisenumber",
            field=models.ForeignKey(
                db_column="CruiseNumber",
                limit_choices_to={"status": True},
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="wwdb.cruise",
                verbose_name="Cruise number",
            ),
        ),
    ]

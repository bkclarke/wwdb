# Generated by Django 4.1.3 on 2024-07-16 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wwdb", "0078_alter_cast_startdate"),
    ]

    operations = [
        migrations.AddField(
            model_name="cast",
            name="wirerinse",
            field=models.BooleanField(
                blank=True, db_column="wirerinse", null=True, verbose_name="Wire rinse"
            ),
        ),
    ]

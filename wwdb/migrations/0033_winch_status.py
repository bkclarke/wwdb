# Generated by Django 4.1.3 on 2022-12-09 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("wwdb", "0032_alter_cast_deploymenttypeid_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="winch",
            name="status",
            field=models.BooleanField(
                blank=True, db_column="Status", null=True, verbose_name="Status"
            ),
        ),
    ]
# Generated by Django 3.1.1 on 2020-09-06 03:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("kinks", "0008_kinklist_short_link"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="customkinklistentry",
            options={"verbose_name_plural": "custom kink list entries"},
        ),
        migrations.AlterModelOptions(
            name="standardkinklistentry",
            options={"verbose_name_plural": "standard kink list entries"},
        ),
    ]

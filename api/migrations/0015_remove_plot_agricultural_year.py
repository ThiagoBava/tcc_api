# Generated by Django 3.2.6 on 2021-11-28 02:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20211128_0205'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plot',
            name='agricultural_year',
        ),
    ]

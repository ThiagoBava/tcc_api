# Generated by Django 3.2.6 on 2021-11-03 22:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_agriculturalyear_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='soilsample',
            name='soil_analysis',
        ),
        migrations.AddField(
            model_name='soilsample',
            name='grid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.grid'),
        ),
    ]

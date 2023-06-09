# Generated by Django 3.2.6 on 2021-10-23 02:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AgriculturalYear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('planting_type', models.BooleanField(default=True)),
                ('planting_date', models.DateTimeField(auto_now_add=True)),
                ('hasvest_date', models.DateTimeField(blank=True, default=None, null=True)),
                ('harvested_bags', models.IntegerField(blank=True, default=0, null=True)),
                ('seed', models.CharField(blank=True, default=None, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BiologicalLabReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('analysis_date', models.DateTimeField(blank=True, default=None, null=True)),
                ('register_date', models.DateTimeField(auto_now_add=True)),
                ('name_lab', models.CharField(default=None, max_length=100)),
                ('report_number_lab', models.CharField(default=None, max_length=100)),
                ('sample_number_lab', models.CharField(default=None, max_length=100)),
                ('cbm', models.FloatField()),
                ('beta_glucosidase', models.FloatField()),
                ('ariphosphatase', models.FloatField()),
                ('acid_phosphatase', models.FloatField()),
                ('organic_matter', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='ChemicalLabReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('analysis_date', models.DateTimeField(blank=True, default=None, null=True)),
                ('register_date', models.DateTimeField(auto_now_add=True)),
                ('name_lab', models.CharField(default=None, max_length=100)),
                ('report_number_lab', models.CharField(default=None, max_length=100)),
                ('sample_number_lab', models.CharField(default=None, max_length=100)),
                ('ph_water', models.FloatField()),
                ('smp', models.FloatField()),
                ('relation_ca_mg', models.FloatField()),
                ('clay', models.FloatField()),
                ('organic_matter', models.FloatField()),
                ('p_mg_l', models.FloatField()),
                ('k_mg_l', models.FloatField()),
                ('ctc_dm_3', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Farm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('owner', models.CharField(max_length=100)),
                ('city', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Grid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.IntegerField(default=1)),
                ('lat', models.CharField(blank=True, default=None, max_length=20)),
                ('lng', models.CharField(blank=True, default=None, max_length=20)),
                ('area_hectare', models.FloatField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PhysicalLabReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('analysis_date', models.DateTimeField(blank=True, default=None, null=True)),
                ('register_date', models.DateTimeField(auto_now_add=True)),
                ('name_lab', models.CharField(default=None, max_length=100)),
                ('report_number_lab', models.CharField(default=None, max_length=100)),
                ('sample_number_lab', models.CharField(default=None, max_length=100)),
                ('sand', models.FloatField(default=0)),
                ('clay', models.FloatField(default=0)),
                ('silt', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='SoilAnalysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agricultural_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.agriculturalyear')),
                ('biological_lab_report', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.biologicallabreport')),
                ('chemical_lab_report', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.chemicallabreport')),
                ('grid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.grid')),
                ('physical_lab_report', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.physicallabreport')),
            ],
        ),
        migrations.CreateModel(
            name='SoilSample',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sample_lat', models.CharField(blank=True, default=None, max_length=20)),
                ('sample_lng', models.CharField(blank=True, default=None, max_length=20)),
                ('accuracy', models.CharField(blank=True, default=None, max_length=20)),
                ('collect_date', models.DateTimeField(default=None)),
                ('weight_g', models.FloatField(blank=True, default=None)),
                ('soil_analysis', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.soilanalysis')),
            ],
        ),
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('npk', models.CharField(blank=True, default=None, max_length=20)),
                ('iqs', models.CharField(blank=True, default=None, max_length=20)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('soil_analysis', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.soilanalysis')),
            ],
        ),
        migrations.CreateModel(
            name='Plot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.IntegerField(default=1)),
                ('area_hectare', models.FloatField(blank=True, default=0, null=True)),
                ('plant_density_hectare', models.IntegerField()),
                ('current_culture', models.CharField(choices=[('corn', 'Milho'), ('soy', 'Soja')], max_length=60)),
                ('first_or_second_planting', models.IntegerField()),
                ('prnt_applied', models.FloatField(blank=True, default=75, null=True)),
                ('predecessor_culture', models.CharField(choices=[('grass', 'Gramínea'), ('legume', 'Leguminosa')], max_length=20)),
                ('yield_expectation_kg', models.IntegerField()),
                ('area_condition', models.CharField(choices=[('in_all_cases', 'Em todos os casos'), ('system_implementation', 'Implantação do sistema'), ('Consolidated_system_no_restriction', 'Consolidado sem restrições'), ('Consolidated_system_with_restriction', 'Consolidado com restrições'), ('Sowing_in_dry_soil', 'Semeadura em solo seco'), ('Pre_germinated_or_seedling_transplant', 'Pré-germinado ou transplante de muda')], max_length=60)),
                ('management_system', models.CharField(choices=[('conventional', 'Convencional'), ('no-till', 'Plantio direto'), ('irrigated rice', 'Arroz irrigado')], max_length=30)),
                ('farm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.farm')),
            ],
        ),
        migrations.AddField(
            model_name='grid',
            name='plot',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.plot'),
        ),
        migrations.AddField(
            model_name='agriculturalyear',
            name='plot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.plot'),
        ),
    ]

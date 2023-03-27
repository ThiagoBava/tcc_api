from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField

from api.models_choices import CULTURE_TO_BE_IMPLEMENTED, MANAGEMENT_SYSTEM, PREDECESSOR_CULTURE, AREA_CONDITION, \
    FIRST_OR_SECOND_PLANTING, PLANTING_TYPE


class Farm(models.Model):
    name = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    city = models.CharField(max_length=100, null=True, default=None, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class Plot(models.Model):
    identifier = models.CharField(max_length=100, null=False, default=1)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, null=False)
    area_hectare = models.FloatField(null=True, default=0, blank=True)
    plant_density_hectare = models.IntegerField()
    current_culture = models.CharField(max_length=60, choices=CULTURE_TO_BE_IMPLEMENTED, blank=False, null=False)
    first_or_second_planting = models.IntegerField(choices=FIRST_OR_SECOND_PLANTING)
    prnt_applied = models.FloatField(null=True, default=75, blank=True)
    predecessor_culture = models.CharField(max_length=20, choices=PREDECESSOR_CULTURE, blank=False, null=False)
    yield_expectation_kg = models.IntegerField()
    area_condition = models.CharField(max_length=60, choices=AREA_CONDITION, blank=False, null=False)
    management_system = models.CharField(max_length=30, choices=MANAGEMENT_SYSTEM, blank=False, null=False)
    agricultural_year = models.JSONField(null=True, blank=True)


class AgriculturalYear(models.Model):
    plot = models.ForeignKey(Plot, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    planting_type = models.CharField(choices=PLANTING_TYPE, default=PLANTING_TYPE[0], max_length=20)
    seed = models.CharField(max_length=100, default=None, blank=True, null=True)
    harvested_bags = models.IntegerField(null=True, default=0, blank=True)
    planting_date = models.DateTimeField(null=True, default=None, blank=True)
    hasvest_date = models.DateTimeField(null=True, default=None, blank=True)


class Grid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    identifier = models.CharField(max_length=20, default=None, blank=True)
    plot = models.ForeignKey(Plot, on_delete=models.CASCADE, null=True)
    lat = models.CharField(max_length=20, default=None, blank=True)
    lng = models.CharField(max_length=20, default=None, blank=True)
    area_hectare = models.FloatField(null=True, default=0, blank=True)


class PhysicalLabReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    grid = models.ForeignKey(Grid, on_delete=models.CASCADE, null=True)
    analysis_date = models.DateTimeField(null=True, default=None, blank=True)
    register_date = models.DateTimeField(null=False, auto_now_add=True, blank=False)
    name_lab = models.CharField(max_length=100, default=None, null=False)
    report_number_lab = models.CharField(max_length=100, default=None)
    sample_number_lab = models.CharField(max_length=100, default=None)
    sand = models.FloatField(default=0, blank=False, null=False)
    clay = models.FloatField(default=0, blank=False, null=False)
    silt = models.FloatField(default=0, blank=False, null=False)


class BiologicalLabReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    grid = models.ForeignKey(Grid, on_delete=models.CASCADE, null=True)
    analysis_date = models.DateTimeField(null=True, default=None, blank=True)
    register_date = models.DateTimeField(null=False, auto_now_add=True, blank=False)
    name_lab = models.CharField(max_length=100, default=None, null=False)
    report_number_lab = models.CharField(max_length=100, default=None)
    sample_number_lab = models.CharField(max_length=100, default=None)
    cbm = models.FloatField()
    beta_glucosidase = models.FloatField()
    ariphosphatase = models.FloatField()
    acid_phosphatase = models.FloatField()
    organic_matter = models.FloatField()


class ChemicalLabReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    grid = models.ForeignKey(Grid, on_delete=models.CASCADE, null=True)
    analysis_date = models.DateTimeField(null=True, default=None, blank=True)
    register_date = models.DateTimeField(null=False, auto_now_add=True, blank=False)
    name_lab = models.CharField(max_length=100, default=None, null=False)
    report_number_lab = models.CharField(max_length=100, default=None)
    sample_number_lab = models.CharField(max_length=100, default=None)

    # LIMING -calagem
    ph_water = models.FloatField()
    smp = models.FloatField()
    relation_ca_mg = models.FloatField()

    # NITROGEN
    clay = models.FloatField()
    organic_matter = models.FloatField()

    # PHOSPHOR
    p_mg_l = models.FloatField()

    # POTASSIUM
    k_mg_l = models.FloatField()
    ctc_dm_3 = models.FloatField()


class SoilAnalysis(models.Model):
    grid = models.ForeignKey(Grid, on_delete=models.CASCADE, null=True)
    physical_lab_report = models.ForeignKey(PhysicalLabReport, on_delete=models.CASCADE, null=True, blank=False)
    biological_lab_report = models.ForeignKey(BiologicalLabReport, on_delete=models.CASCADE, null=True, blank=False)
    chemical_lab_report = models.ForeignKey(ChemicalLabReport, on_delete=models.CASCADE, null=True, blank=False)
    agricultural_year = models.ForeignKey(AgriculturalYear, on_delete=models.CASCADE, null=False)
    register_date = models.DateTimeField(null=False, auto_now_add=True, blank=False)


class SoilSample(models.Model):
    grid = models.ForeignKey(Grid, on_delete=models.CASCADE, null=True)
    sample_lat = models.CharField(max_length=20, default=None, blank=True)
    sample_lng = models.CharField(max_length=20, default=None, blank=True)
    accuracy = models.CharField(max_length=20, default=None, blank=True)
    collect_date = models.DateTimeField(null=False, default=None, blank=False)
    weight_g = models.FloatField(default=None, blank=True)


class Recommendation(models.Model):
    soil_analysis = models.ForeignKey(SoilAnalysis, on_delete=models.CASCADE, null=True)
    npk = models.JSONField(null=True, blank=True)
    iqs = models.JSONField(null=True, blank=True)
    soil_class = models.JSONField(null=True, blank=True)
    mineral_fertilizer = models.JSONField(null=True, blank=True)
    date = models.DateTimeField(null=False, auto_now_add=True, blank=False)


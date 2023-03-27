"""É possível a criação de serializer somente para exibição de campos especificos, relacionando outros modelos"""
import datetime

from django.contrib.auth.models import User
from django.conf import settings
from rest_framework import serializers
from api.models import Farm, AgriculturalYear, Plot, Grid, SoilAnalysis, SoilSample, Recommendation, \
    ChemicalLabReport, PhysicalLabReport, BiologicalLabReport
from api.models_choices import PLANTING_TYPE, CULTURE_TO_BE_IMPLEMENTED
from api.validators import func_to_valid_serializer, validate_agricultural_year_period


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'is_superuser', 'username', 'email', 'is_active']


class FarmSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Farm
        fields = '__all__'


class PlotSerializer(serializers.ModelSerializer):
    farm = FarmSerializer(many=False, read_only=True)

    class Meta:
        model = Plot
        fields = '__all__'


class AgriculturalYearSerializer(serializers.ModelSerializer):
    plot = PlotSerializer(many=False, read_only=True)
    planting_date = serializers.DateTimeField(input_formats=settings.DATE_INPUT_FORMATS, allow_null=True, default=None)
    hasvest_date = serializers.DateTimeField(input_formats=settings.DATE_INPUT_FORMATS, allow_null=True, default=None)
    name = serializers.SerializerMethodField()

    class Meta:
        model = AgriculturalYear
        fields = '__all__'

    def get_name(self, obj):
        return dict(PLANTING_TYPE)[obj.planting_type]


class GridSerializer(serializers.ModelSerializer):
    plot = PlotSerializer(many=False, read_only=True)
    plot_name = serializers.SerializerMethodField()

    class Meta:
        model = Grid
        fields = '__all__'

    def get_plot_name(self, obj):
        return obj.plot.identifier + ' - ' + obj.plot.farm.name


class ChemicalLabReportSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    register_date = serializers.DateTimeField(input_formats=settings.DATE_INPUT_FORMATS)
    analysis_date = serializers.DateTimeField(input_formats=settings.DATE_INPUT_FORMATS)
    name = serializers.SerializerMethodField()
    farm_name = serializers.SerializerMethodField()
    grid_identifier = serializers.SerializerMethodField()
    farm = serializers.SerializerMethodField()
    grid = GridSerializer(many=False, read_only=True)

    class Meta:
        model = ChemicalLabReport
        fields = '__all__'

    def get_name(self, obj):
        return obj.analysis_date.strftime('%d/%m/%Y')+' - '+obj.name_lab+' - '+obj.report_number_lab+' - '+obj.sample_number_lab

    def get_farm(self, obj):
        return obj.grid.plot.farm.id

    def get_farm_name(self, obj):
        return obj.grid.plot.farm.name

    def get_grid_identifier(self, obj):
        return obj.grid.identifier


class PhysicalLabReportSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    grid = GridSerializer(many=False, read_only=True)
    register_date = serializers.DateTimeField(input_formats=settings.DATE_INPUT_FORMATS, default=datetime.datetime.now())
    analysis_date = serializers.DateTimeField(input_formats=settings.DATE_INPUT_FORMATS, default=datetime.datetime.now())
    name = serializers.SerializerMethodField()
    farm = serializers.SerializerMethodField()

    class Meta:
        model = PhysicalLabReport
        fields = '__all__'

    def get_name(self, obj):
        return obj.analysis_date.strftime('%d/%m/%Y')+' - '+obj.name_lab+' - '+obj.report_number_lab+' - '+obj.sample_number_lab

    def get_farm(self, obj):
        return obj.grid.plot.farm.id


class BiologicalLabReportSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    grid = GridSerializer(many=False, read_only=True)
    register_date = serializers.DateTimeField(input_formats=settings.DATE_INPUT_FORMATS, allow_null=True, required=False, default=None)
    analysis_date = serializers.DateTimeField(input_formats=settings.DATE_INPUT_FORMATS, allow_null=True, required=False, default=None)
    name = serializers.SerializerMethodField()
    farm = serializers.SerializerMethodField()

    class Meta:
        model = BiologicalLabReport
        fields = '__all__'

    def get_name(self, obj):
        return obj.analysis_date.strftime('%d/%m/%Y')+' - '+obj.name_lab+' - '+obj.report_number_lab+' - '+obj.sample_number_lab

    def get_farm(self, obj):
        return obj.grid.plot.farm.id


class SoilAnalysisSerializer(serializers.ModelSerializer):
    grid = GridSerializer(many=False, read_only=True)
    agricultural_year = AgriculturalYearSerializer(many=False, read_only=True)
    physical_lab_report = PhysicalLabReportSerializer(many=False, read_only=True)
    biological_lab_report = BiologicalLabReportSerializer(many=False, read_only=True)
    chemical_lab_report = ChemicalLabReportSerializer(many=False, read_only=True)
    register_date = serializers.DateTimeField(input_formats=settings.DATE_INPUT_FORMATS)
    farm = serializers.SerializerMethodField(source='grid')

    class Meta:
        model = SoilAnalysis
        fields = '__all__'

    def get_farm(self, obj):
        return {"id": obj.grid.plot.farm.id, "name": obj.grid.plot.farm.name}


class SoilSampleSerializer(serializers.ModelSerializer):
    grid = GridSerializer(many=False, read_only=True)
    date = serializers.DateTimeField(input_formats=settings.DATE_INPUT_FORMATS)

    class Meta:
        model = SoilSample
        fields = '__all__'


class RecommendationSerializer(serializers.ModelSerializer):
    soil_analysis = SoilAnalysisSerializer(many=False, read_only=True)
    date = serializers.DateTimeField(input_formats=settings.DATE_INPUT_FORMATS)

    class Meta:
        model = Recommendation
        fields = '__all__'
        actions_readonly_fields = {
            ('update', 'partial_update'): ('client', )
        }


class Plot_Farm_Serializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Plot
        fields = '__all__'

    def get_name(self, obj):
        return obj.identifier+' - '+obj.farm.name


class AgriculturalYear_Plot_Serializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = AgriculturalYear
        fields = '__all__'

    def get_name(self, obj):
        return obj.plot.identifier+' - '+obj.plot.farm.name+' - '+obj.seed+' - '+obj.planting_date.strftime('%d/%m/%Y')


class AgriculturalYear_User_Serializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = AgriculturalYear
        fields = '__all__'

    def get_name(self, obj):
        d = None
        if obj.planting_date is not None:
            d = obj.planting_date.strftime('%d/%m/%Y')
        return f"{dict(PLANTING_TYPE)[obj.planting_type]} {dict(CULTURE_TO_BE_IMPLEMENTED)[obj.seed]} {d if d else ''}"


class Grid_Plot_Serializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Grid
        fields = '__all__'

    def get_name(self, obj):
        return obj.plot.identifier+' - '+obj.plot.farm.name+' - '+str(obj.identifier)+' - '+str(obj.area_hectare)+'ha'


class SoilAnalysis_Grid_AgriculturalYear_Serializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Grid
        fields = '__all__'

    def get_name(self, obj):
        return str(obj.grid.identifier)+' - '+str(obj.grid.area_hectare)+'ha - '+obj.agricultural_year.seed+' - '\
            +obj.agricultural_year.planting_date.strftime('%d/%m/%Y')


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
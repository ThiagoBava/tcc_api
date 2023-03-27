from django.contrib import admin
from api.models import Farm, AgriculturalYear, Plot, Grid, SoilSample, Recommendation, ChemicalLabReport, BiologicalLabReport, PhysicalLabReport

page_counter = 10

class Farms(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'city', 'user')
    list_display_links = list_display
    search_fields = list_display
    list_per_page = page_counter


class AgriculturalYears(admin.ModelAdmin):
    list_display = ('id', 'plot', 'planting_type', 'planting_date', 'hasvest_date', 'harvested_bags', 'seed')
    list_display_links = list_display
    search_fields = list_display
    list_per_page = page_counter


class Plots(admin.ModelAdmin):
    list_display = ('id', 'identifier', 'farm', 'area_hectare', 'plant_density_hectare', 'current_culture', 'first_or_second_planting', 
                    'prnt_applied', 'predecessor_culture', 'yield_expectation_kg', 'area_condition', 'management_system')
    list_display_links = list_display
    search_fields = list_display
    list_per_page = page_counter


class Grids(admin.ModelAdmin):
    list_display = ('id', 'identifier', 'plot', 'lat', 'lng', 'area_hectare')
    list_display_links = list_display
    search_fields = list_display
    list_per_page = page_counter


class SoilSamples(admin.ModelAdmin):
    list_display = ('id', 'grid', 'sample_lat', 'sample_lng', 'accuracy', 'collect_date', 'weight_g')
    list_display_links = list_display
    search_fields = list_display
    list_per_page = page_counter


class Recommendations(admin.ModelAdmin):
    list_display = ('id', 'soil_analysis', 'npk', 'iqs', 'date')
    list_display_links = list_display
    search_fields = list_display
    list_per_page = page_counter


class ChemicalLabReports(admin.ModelAdmin):
    list_display = ('id', 'analysis_date', 'register_date', 'name_lab', 'report_number_lab', 'sample_number_lab', 
                    'ph_water', 'smp', 'relation_ca_mg', 'clay', 'organic_matter', 'p_mg_l', 'k_mg_l', 'ctc_dm_3')
    list_display_links = list_display
    search_fields = list_display
    list_per_page = page_counter

    
class PhysicalLabReports(admin.ModelAdmin):
    list_display = ('id', 'analysis_date', 'register_date', 'name_lab', 'report_number_lab', 'sample_number_lab', 
                    'sand', 'clay', 'silt')
    list_display_links = list_display
    search_fields = list_display
    list_per_page = page_counter


class BiologicalLabReports(admin.ModelAdmin):
    list_display = ('id', 'analysis_date', 'register_date', 'name_lab', 'report_number_lab', 'sample_number_lab', 
                    'cbm', 'beta_glucosidase', 'ariphosphatase', 'acid_phosphatase', 'organic_matter')
    list_display_links = list_display
    search_fields = list_display
    list_per_page = page_counter


admin.site.register(Farm, Farms)
admin.site.register(Plot, Plots)
admin.site.register(AgriculturalYear, AgriculturalYears)
admin.site.register(Grid, Grids)
admin.site.register(SoilSample, SoilSamples)
admin.site.register(Recommendation, Recommendations)
admin.site.register(ChemicalLabReport, ChemicalLabReports)
admin.site.register(PhysicalLabReport, PhysicalLabReports)
admin.site.register(BiologicalLabReport, BiologicalLabReports)
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from api.api_views.agricultural_year_view import AgriculturalYearSearchByNameViewSet, AgriculturalYearsViewSet, \
    AgriculturalYearSearchByUserViewSet
from api.api_views.farm_view import FarmSearchByNameViewSet, FarmsViewSet
from api.api_views.plot_view import PlotSearchByNameViewSet, PlotsViewSet
from api.api_views.grid_view import GridSearchByNameViewSet, GridsViewSet, GridSearchByFarmViewSet
from api.api_views.soil_sample_view import SoilSamplesViewSet
from api.api_views.soil_analysis_view import SoilAnalysesSearchByNameViewSet, SoilAnalysesViewSet
from api.api_views.recommendation_view import RecommendationsViewSet, OrganicRecommendationsViewSet, \
    MineralRecommendationsViewSet
from api.api_views.lab_reports_view import ChemicalLabReportsSerializerViewSet, \
    PhysicalLabReportsSerializerViewSet, BiologicalLabReportsSerializerViewSet, \
    ChemicalLabReportSearchByNameViewSet, PhysicalLabReportSearchByNameViewSet, \
    BiologicalLabReportSearchByNameViewSet, ChemicalLabReportSearchByGridViewSet, \
    PhysicalLabReportSearchByGridViewSet, BiologicalLabReportSearchByGridViewSet

from api.views import RegisterViewSet



router = routers.DefaultRouter()
# SEARCHERS
router.register('api/farm/search-by-name', FarmSearchByNameViewSet, basename='Buscar propriedade pelo nome')
router.register('api/plot/search-by-name', PlotSearchByNameViewSet, basename='Buscar talhão pelo nome')
router.register('api/agricultural-year/search-by-name', AgriculturalYearSearchByNameViewSet, basename='Buscar ano agrícola nome')
router.register('api/agricultural-year/search-by-user', AgriculturalYearSearchByUserViewSet, basename='Buscar ano agrícola nome')
router.register('api/grid/search-by-name', GridSearchByNameViewSet, basename='Buscar grid pelo nome')
router.register('api/grid/search-by-farm', GridSearchByFarmViewSet, basename='Buscar grid pela propriedade')
router.register('api/soil-analysis/search-by-name', SoilAnalysesSearchByNameViewSet, basename='Buscar análise do solo pelo nome')
router.register('api/chemical-lab-report/search-by-name', ChemicalLabReportSearchByNameViewSet, basename='Buscar relatório laboratorial químico pelo nome')
router.register('api/physical-lab-report/search-by-name', PhysicalLabReportSearchByNameViewSet, basename='Buscar relatório laboratorial físico pelo nome')
router.register('api/biological-lab-report/search-by-name', BiologicalLabReportSearchByNameViewSet, basename='Buscar relatório laboratorial biológico pelo nome')
router.register('api/chemical-lab-report/search-by-grid', ChemicalLabReportSearchByGridViewSet, basename='Buscar relatório laboratorial químico pela grid')
router.register('api/physical-lab-report/search-by-grid', PhysicalLabReportSearchByGridViewSet, basename='Buscar relatório laboratorial físico pela grid')
router.register('api/biological-lab-report/search-by-grid', BiologicalLabReportSearchByGridViewSet, basename='Buscar relatório laboratorial biológico pela grid')
# APIS
router.register('api/farm', FarmsViewSet, basename='Propriedade')
router.register('api/agricultural-year', AgriculturalYearsViewSet, basename='Ano agrícola')
router.register('api/plot', PlotsViewSet, basename='Talhão')
router.register('api/grid', GridsViewSet, basename='Grid')
router.register('api/chemical-lab-report', ChemicalLabReportsSerializerViewSet, basename='Análise clínica Qímica')
router.register('api/physical-lab-report', PhysicalLabReportsSerializerViewSet, basename='Análise clínica Física')
router.register('api/biological-lab-report', BiologicalLabReportsSerializerViewSet, basename='Análise clínica Biológica')
router.register('api/soil-analysis', SoilAnalysesViewSet, basename='Amostra de Solo')
router.register('api/soil-sample', SoilSamplesViewSet, basename='Amostra de Solo')
router.register('api/recommendation', RecommendationsViewSet, basename='Recomendação')
router.register('api/organic-recommendation', OrganicRecommendationsViewSet, basename='Recomendação orgânica')
router.register('api/mineral-recommendation', MineralRecommendationsViewSet, basename='Recomendação orgânica')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', obtain_auth_token, name='api_token_auth'),
    path('api/register/', RegisterViewSet.as_view({'post': 'create'})),
    path('', include(router.urls))
]

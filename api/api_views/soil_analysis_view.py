from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from api.models import AgriculturalYear, BiologicalLabReport, ChemicalLabReport, Farm, Grid, PhysicalLabReport, Plot, SoilAnalysis
from api.serializer import SoilAnalysis_Grid_AgriculturalYear_Serializer, SoilAnalysisSerializer


class SoilAnalysesViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = SoilAnalysisSerializer 

    def get_queryset(self):
        filter_user = get_user_filter_soil_analysis(self.request.user)
        return SoilAnalysis.objects.filter(filter_user)

    def create(self, request, *args, **kwargs):
        serializer = SoilAnalysisSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sa_obj = serializer.save(
            grid=Grid.objects.get(pk=request.data['grid']['id']),
            agricultural_year=AgriculturalYear.objects.get(pk=request.data['agricultural_year']['id'])
        )
        sa_obj = self.set_lab_reports_save(sa_obj, request.data)
        sa_obj.save()
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        instance = self.set_lab_reports_update(instance, request.data)
        instance.grid=Grid.objects.get(pk=request.data['grid']['id'])
        instance.agricultural_year=AgriculturalYear.objects.get(pk=request.data['agricultural_year']['id'])
        serializer = SoilAnalysisSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance, serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def set_lab_reports_save(self, obj, request_data):
        if ('physical_lab_report' in request_data):
            obj.physical_lab_report=PhysicalLabReport.objects.get(pk=request_data['physical_lab_report']['id'])
        if ('biological_lab_report' in request_data):
            obj.biological_lab_report=BiologicalLabReport.objects.get(pk=request_data['biological_lab_report']['id'])
        if ('chemical_lab_report' in request_data):
            obj.chemical_lab_report=ChemicalLabReport.objects.get(pk=request_data['chemical_lab_report']['id'])
        return obj


    def set_lab_reports_update(self, instance, request_data):
        if ('physical_lab_report' in request_data):
            instance.physical_lab_report=PhysicalLabReport.objects.get(pk=request_data['physical_lab_report']['id'])
        if ('biological_lab_report' in request_data):
            instance.biological_lab_report=BiologicalLabReport.objects.get(pk=request_data['biological_lab_report']['id'])
        if ('chemical_lab_report' in request_data):
            instance.chemical_lab_report=ChemicalLabReport.objects.get(pk=request_data['chemical_lab_report']['id'])
        return instance


class SoilAnalysesSearchByNameViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = SoilAnalysis_Grid_AgriculturalYear_Serializer

    def get_queryset(self):
        term = self.request.GET.get('searchTerm', '')
        filter_user = get_user_filter_soil_analysis(self.request.user)
        prefetch_gf = Grid.objects.filter(Q(identifier__icontains=term) | Q(area_hectare__icontains=term))
        prefetch_ayf = AgriculturalYear.objects.filter(Q(planting_date__icontains=term) | Q(seed__icontains=term))
        queryset = SoilAnalysis.objects.filter((Q(grid__in=prefetch_gf) | Q(agricultural_year__in=prefetch_ayf))
                    & filter_user)
        return queryset


def get_user_filter_soil_analysis(user_auth):
    prefetch_f = Farm.objects.filter(user=user_auth)
    prefetch_p = Plot.objects.filter(farm__in=prefetch_f)
    prefetch_g = Grid.objects.filter(plot__in=prefetch_p)
    prefetch_ay = AgriculturalYear.objects.filter(plot__in=prefetch_p)
    return Q(grid__in=prefetch_g) & Q(agricultural_year__in=prefetch_ay)


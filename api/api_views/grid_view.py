import datetime

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.db.models import Q

from api.models import AgriculturalYear, Farm, Grid, Plot
from api.serializer import Grid_Plot_Serializer, GridSerializer, SoilAnalysisSerializer


class GridsViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = GridSerializer

    def get_queryset(self):
        filter_user = get_user_filter_grid(self.request.user)
        return Grid.objects.filter(filter_user)

    def create(self, request, *args, **kwargs):
        serializer = GridSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            user=self.request.user,
            plot=Plot.objects.get(pk=request.data['plot']['id'])
        )
        # create_soil_analysis(serializer.instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        instance.plot = Plot.objects.get(pk=request.data['plot']['id'])
        serializer = GridSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance, serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GridSearchByNameViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = Grid_Plot_Serializer

    def get_queryset(self):
        term = self.request.GET.get('searchTerm', '')
        filter_user = get_user_filter_grid(self.request.user)
        prefetch_pf = Plot.objects.filter(identifier__icontains=term)
        queryset = Grid.objects.filter(Q(Q(identifier__icontains=term)
                    | Q(area_hectare__icontains=term) | Q(plot__in=prefetch_pf)) & filter_user)
        return queryset


class GridSearchByFarmViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = Grid_Plot_Serializer

    def get_queryset(self):
        term = self.request.GET.get('id', '')
        queryset = Grid.objects.filter(plot__farm_id=term)
        return queryset


def get_user_filter_grid(user_auth):
    prefetch_f = Farm.objects.filter(user=user_auth)
    prefetch_p = Plot.objects.filter(farm__in=prefetch_f)
    return Q(plot__in=prefetch_p)


def create_soil_analysis(grid_instance):
    soil_analysis = SoilAnalysisSerializer(data={
        'register_date': datetime.datetime.now()
    })
    soil_analysis.is_valid(raise_exception=True)
    soil_analysis.save(
        grid=grid_instance,
        agricultural_year=AgriculturalYear.objects.get(plot=grid_instance.plot)
    )


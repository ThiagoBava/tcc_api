from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from api.models import AgriculturalYear, Plot, Farm
from api.serializer import AgriculturalYearSerializer, Plot_Farm_Serializer, PlotSerializer


class PlotsViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = PlotSerializer

    def get_queryset(self):
        filter_user = get_user_filter_plot(self.request.user)
        return Plot.objects.filter(filter_user)

    def create(self, request, *args, **kwargs):
        serializer = PlotSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            farm=Farm.objects.get(pk=request.data['farm']['id'])
        )
        update_agricultural_year(request.data['agricultural_year']['id'], serializer.instance, **kwargs)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        instance.farm = Farm.objects.get(pk=request.data['farm']['id'])
        serializer = PlotSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance, serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PlotSearchByNameViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = Plot_Farm_Serializer

    def get_queryset(self):
        term = self.request.GET.get('searchTerm', '')
        filter_user = get_user_filter_plot(self.request.user)
        prefetch_ff = Farm.objects.filter(name__icontains=term)
        queryset = Plot.objects.filter((Q(identifier__icontains=term)
                    | Q(farm__in=prefetch_ff)) & filter_user)
        return queryset


def get_user_filter_plot(user_auth):
    prefetch_f = Farm.objects.filter(user=user_auth)
    return Q(farm__in=prefetch_f)


def update_agricultural_year(id, plot_instance, **kwargs):
    partial = kwargs.pop('partial', False)
    agricultural_year = AgriculturalYear.objects.get(pk=id)
    agricultural_year.plot=plot_instance
    ay_serializer = AgriculturalYearSerializer(agricultural_year, data=agricultural_year.__dict__, partial=partial)
    ay_serializer.is_valid(raise_exception=True)
    ay_serializer.update(agricultural_year, ay_serializer.validated_data)


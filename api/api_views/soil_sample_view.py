from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from api.models import AgriculturalYear, Farm, Grid, Plot, SoilSample
from api.serializer import SoilSampleSerializer


class SoilSamplesViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = SoilSampleSerializer 

    def get_queryset(self):
        filter_user = get_user_filter_soil_sample(self.request.user)
        return SoilSample.objects.filter(filter_user)

    def create(self, request, *args, **kwargs):
        serializer = SoilSampleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            grid=Grid.objects.get(pk=request.data['grid']['id'])
        )
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        instance.grid=Grid.objects.get(pk=request.data['grid']['id'])
        serializer = SoilSampleSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance, serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_200_OK)


def get_user_filter_soil_sample(user_auth):
    prefetch_f = Farm.objects.filter(user=user_auth)
    prefetch_p = Plot.objects.filter(farm__in=prefetch_f)
    prefetch_g = Grid.objects.filter(plot__in=prefetch_p)
    return Q(grid__in=prefetch_g)


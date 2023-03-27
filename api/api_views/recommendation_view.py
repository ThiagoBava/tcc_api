from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from api.models import AgriculturalYear, Farm, Grid, Plot, SoilAnalysis, Recommendation
from api.serializer import RecommendationSerializer
from api.services.fertilizing_service import FertilizingService
from api.services.soil_quality_service import SoilQualityService


class RecommendationsViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = RecommendationSerializer 
    http_method_names = ['get', 'post', 'head', 'delete']

    def get_queryset(self):
        filter_user = get_user_filter_soil_sample(self.request.user)
        return Recommendation.objects.filter(filter_user)

    def create(self, request, *args, **kwargs):
        serializer = RecommendationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        soil_analysis=SoilAnalysis.objects.get(pk=request.data['soil_analysis']['id'])
        npk = FertilizingService().generate_npk(soil_analysis)
        iqs = SoilQualityService().generate_iqs(soil_analysis)
        soil_class = SoilQualityService().classify_soil(soil_analysis)
        serializer.save(
            soil_analysis=soil_analysis,
            npk=npk,
            iqs=iqs,
            soil_class=soil_class
        )
        return Response(serializer.data)


def get_user_filter_soil_sample(user_auth):
    prefetch_f = Farm.objects.filter(user=user_auth)
    prefetch_p = Plot.objects.filter(farm__in=prefetch_f)
    prefetch_g = Grid.objects.filter(plot__in=prefetch_p)
    prefetch_ay = AgriculturalYear.objects.filter(plot__in=prefetch_p)
    prefetch_sa = SoilAnalysis.objects.filter(Q(grid__in=prefetch_g) & Q(agricultural_year__in=prefetch_ay))
    return Q(soil_analysis__in=prefetch_sa)


class OrganicRecommendationsViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = RecommendationSerializer
    http_method_names = ['get', 'post', 'head', 'delete']

    def create(self, request, *args, **kwargs):
        ret = FertilizingService().generate_organic_fertilizer(request)

        return Response(ret, status=status.HTTP_200_OK)


class MineralRecommendationsViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = RecommendationSerializer
    http_method_names = ['get', 'post', 'head', 'delete']

    def create(self, request, *args, **kwargs):
        ret = FertilizingService().generate_mineral_fertilizer(request)
        return Response(ret, status=status.HTTP_200_OK)

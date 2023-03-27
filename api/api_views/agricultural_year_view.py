from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.db.models import Q
from django.contrib.auth.models import User

from api.models import AgriculturalYear, Farm, Plot
from api.serializer import AgriculturalYear_Plot_Serializer, AgriculturalYear_User_Serializer, AgriculturalYearSerializer, Plot_Farm_Serializer


class AgriculturalYearsViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = AgriculturalYearSerializer

    def get_queryset(self):
        filter_user = get_user_filter_agricultural_year(self.request.user)
        return AgriculturalYear.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = AgriculturalYearSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            user=User.objects.get(pk=request.user.id)
            # plot=Plot.objects.get(pk=request.data['plot']['id'])
        )
        return Response(serializer.data)
    #
    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     instance.plot = Plot.objects.get(pk=request.data['plot']['id'])
    #     serializer = AgriculturalYearSerializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.update(instance, serializer.validated_data)
    #     return Response(serializer.data, status=status.HTTP_200_OK)


class AgriculturalYearSearchByNameViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = AgriculturalYear_Plot_Serializer

    def get_queryset(self):
        term = self.request.GET.get('searchTerm', '')
        filter_user = get_user_filter_agricultural_year(self.request.user)
        prefetch_pf = Plot.objects.filter(identifier__icontains=term)
        queryset = AgriculturalYear.objects.filter(Q(Q(planting_date__icontains=term)
                    | Q(seed__icontains=term) | Q(plot__in=prefetch_pf)) & filter_user)
        return queryset


def get_user_filter_agricultural_year(user_auth):
    prefetch_f = Farm.objects.filter(user=user_auth)
    prefetch_p = Plot.objects.filter(farm__in=prefetch_f)
    return Q(plot__in=prefetch_p)


class AgriculturalYearSearchByUserViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = AgriculturalYear_User_Serializer

    def get_queryset(self):
        term = self.request.GET.get('searchTerm', '')
        queryset = AgriculturalYear.objects.filter(user=self.request.user)
        return queryset
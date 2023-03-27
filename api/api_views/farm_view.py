from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from django.contrib.auth.models import User

from api.models import Farm
from api.serializer import FarmSerializer


class FarmsViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = FarmSerializer
    
    def get_queryset(self):
        return Farm.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = FarmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            user=User.objects.get(pk=request.user.id)
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = FarmSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance, serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FarmSearchByNameViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = FarmSerializer

    def get_queryset(self):
        return Farm.objects.filter(name__icontains=self.request.GET.get('searchTerm', ''), user=self.request.user)


from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from api.models import SoilSample, \
    Recommendation, PhysicalLabReport, BiologicalLabReport
from api.serializer import SoilSampleSerializer, RecommendationSerializer, PhysicalLabReportSerializer, \
    BiologicalLabReportSerializer, RegisterUserSerializer


class SoilSamplesViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = SoilSample.objects.all()
    serializer_class = SoilSampleSerializer


class RecommendationsViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer


class PhysicalLabReportSerializerViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = PhysicalLabReport.objects.all()
    serializer_class = PhysicalLabReportSerializer


class BiologicalLabReportSerializerViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = BiologicalLabReport.objects.all()
    serializer_class = BiologicalLabReportSerializer


class RegisterViewSet(viewsets.GenericViewSet):
    permission_classes = (AllowAny,)

    def create(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email']
        )
        user.set_password(serializer.validated_data['password'])
        user.save()
        return Response({
            'user_id': user.pk,
            'email': user.email
        })

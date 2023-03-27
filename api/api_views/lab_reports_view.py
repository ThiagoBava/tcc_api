from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.db.models import Q
from api.models import BiologicalLabReport, ChemicalLabReport, PhysicalLabReport, Grid

from api.serializer import BiologicalLabReportSerializer, ChemicalLabReportSerializer, PhysicalLabReportSerializer


class ChemicalLabReportsSerializerViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ChemicalLabReportSerializer

    def get_queryset(self):
        return ChemicalLabReport.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = ChemicalLabReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user, grid=Grid.objects.get(pk=self.request.data['grid']))
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = ChemicalLabReportSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance, serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PhysicalLabReportsSerializerViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = PhysicalLabReportSerializer

    def get_queryset(self):
        return PhysicalLabReport.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = PhysicalLabReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user, grid=Grid.objects.get(id=request.data['grid']['id']))
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = PhysicalLabReportSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance, serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BiologicalLabReportsSerializerViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = BiologicalLabReportSerializer

    def get_queryset(self):
        return BiologicalLabReport.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = BiologicalLabReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user, grid=Grid.objects.get(id=self.request.data['grid']['id']))
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = BiologicalLabReportSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance, serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChemicalLabReportSearchByNameViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ChemicalLabReportSerializer

    def get_queryset(self):
        term = self.request.GET.get('searchTerm', '')
        queryset = ChemicalLabReport.objects.filter(Q(Q(analysis_date__icontains=term) 
                    | Q(name_lab__icontains=term) | Q(report_number_lab__icontains=term) | Q(sample_number_lab__icontains=term))
                    & Q(user=self.request.user))
        return queryset


class PhysicalLabReportSearchByNameViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = PhysicalLabReportSerializer

    def get_queryset(self):
        term = self.request.GET.get('searchTerm', '')
        queryset = PhysicalLabReport.objects.filter(Q(Q(analysis_date__icontains=term) 
                    | Q(name_lab__icontains=term) | Q(report_number_lab__icontains=term) | Q(sample_number_lab__icontains=term))
                    & Q(user=self.request.user))
        return queryset


class BiologicalLabReportSearchByNameViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = BiologicalLabReportSerializer

    def get_queryset(self):
        term = self.request.GET.get('searchTerm', '')
        queryset = BiologicalLabReport.objects.filter(Q(Q(analysis_date__icontains=term) 
                    | Q(name_lab__icontains=term) | Q(report_number_lab__icontains=term) | Q(sample_number_lab__icontains=term))
                    & Q(user=self.request.user))
        return queryset

class ChemicalLabReportSearchByGridViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ChemicalLabReportSerializer

    def get_queryset(self):
        term = self.request.GET.get('id', '')
        queryset = ChemicalLabReport.objects.filter(grid=term)
        return queryset


class PhysicalLabReportSearchByGridViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = PhysicalLabReportSerializer

    def get_queryset(self):
        term = self.request.GET.get('id', '')
        queryset = PhysicalLabReport.objects.filter(grid=term)
        return queryset


class BiologicalLabReportSearchByGridViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = BiologicalLabReportSerializer

    def get_queryset(self):
        term = self.request.GET.get('id', '')
        queryset = BiologicalLabReport.objects.filter(grid=term)
        return queryset
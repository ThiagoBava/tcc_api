from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.models import ChemicalLabReport
from api.serializer import ChemicalLabReportSerializer


class ChemicalLabReportSerializerViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = ChemicalLabReport.objects.all()
    serializer_class = ChemicalLabReportSerializer

    # def retrieve(self, request, *args, **kwargs):
    #     implementar o get para pegar o grid e talhao


from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .serailizers import PatientRegisterSerializer
from .models import Patient


class PatientViewSet(viewsets.ModelViewSet):
    queryset=Patient.objects.all()
    serializer_class=PatientRegisterSerializer
    
    
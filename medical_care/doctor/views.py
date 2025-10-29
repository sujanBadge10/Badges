

# Create your views here.
from rest_framework.response import Response
from .models import Doctor
from .serializers import DoctorRegisterSerializer
from rest_framework import viewsets
from .serializers import DoctorRegisterSerializer
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import BasicAuthentication
from .CustomPermission import DoctorPermission

# -------------------------------
# Doctor Registration View
# -------------------------------
class DoctorRegisterView(viewsets.ModelViewSet):
   
    queryset = Doctor.objects.all()
    serializer_class = DoctorRegisterSerializer
    permission_classes = [permissions.AllowAny]  # Doctors can self-register
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                "doctor": serializer.data,
                "message": "Registration successful! "
                           "Your account is not active yet. "
                           "Please wait for admin approval."
            },
            headers=headers
        )
        
class DoctorViewSet(viewsets.ModelViewSet):
    """
    List, retrieve, update, delete doctors.
    Admin can approve doctor accounts (is_verified=True)
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorRegisterSerializer  # you can use a separate serializer if needed
    authentication_classes=[BasicAuthentication]
    permission_classes=[DoctorPermission]

    
    # @action(detail=True, methods=["post"], permission_classes=[permissions.IsAdminUser])
    # def approve(self, request, pk=None):
    #     """
    #     Admin can approve a doctor account.
    #     """
    #     doctor = self.get_object()
    #     doctor.is_verified = True
    #     doctor.save()
    #     return Response({"message": f"Doctor {doctor.user.username} has been approved."})
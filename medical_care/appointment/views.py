from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from datetime import datetime
from .models import Appointment
from doctor.models import Doctor
from .serailizers import AppointmentSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Appointment.objects.all()
        elif hasattr(user, "doctor"):
            return Appointment.objects.filter(doctor=user.doctor)
        elif hasattr(user, "patient"):
            return Appointment.objects.filter(patient=user.patient)
        return Appointment.objects.none()

    @action(detail=False, methods=["get"], permission_classes=[permissions.AllowAny])
    def busy_slots(self, request):
        """
        Example: /api/appointment/busy_slots/?doctor_id=1&date=2025-09-15
        Returns all booked times for that doctor on that date
        """
        doctor_id = request.query_params.get("doctor_id")
        date_str = request.query_params.get("date")

        if not doctor_id or not date_str:
            return Response(
                {"error": "doctor_id and date are required params"},
                status=400
            )

        try:
            doctor = Doctor.objects.get(id=doctor_id)
        except Doctor.DoesNotExist:
            return Response({"error": "Doctor not found"}, status=404)

        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)

        appointments = Appointment.objects.filter(doctor=doctor, date=date)
        busy_times = [appt.time.strftime("%H:%M") for appt in appointments]

        return Response({
            "doctor": doctor.user.get_full_name(),
            "date": date_str,
            "busy_slots": busy_times
        })

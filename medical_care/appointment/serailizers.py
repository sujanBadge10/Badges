from rest_framework import serializers
from .models import Appointment
from doctor.models import Doctor
from datetime import datetime


class AppointmentSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source="doctor.user.get_full_name", read_only=True)
    patient_name = serializers.CharField(source="patient.get_full_name", read_only=True)

    class Meta:
        model = Appointment
        fields = [
            "id", "doctor", "doctor_name", "patient", "patient_name",
            "date", "time", "status", "created_at"
        ]
        read_only_fields = ["id", "status", "created_at", "patient"]

    def validate(self, data):
        doctor = data["doctor"]
        date = data["date"]
        time = data["time"]

        # 1️⃣ Date must be in the future
        if date < datetime.now().date():
            raise serializers.ValidationError("Appointment date must be in the future.")

        # 2️⃣ Time must be inside doctor working hours
        start_time = doctor.start_time
        end_time = doctor.end_time

        if not (start_time <= time <= end_time):
            raise serializers.ValidationError(
                f"Doctor is only available between ."
            )

        # 3️⃣ No double booking
        if Appointment.objects.filter(doctor=doctor, date=date, time=time).exists():
            raise serializers.ValidationError("This time slot is already booked.")

        return data

    def create(self, validated_data):
    # Assign current user as patient
        patient = self.context["request"].user.patient  # ✅ get Patient instance
        validated_data["patient"] = patient
        return super().create(validated_data)

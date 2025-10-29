from rest_framework import serializers
from core.models import CustomUser
from .models import Patient


class PatientRegisterSerializer(serializers.ModelSerializer):
    # User fields
    first_name=serializers.CharField(source="user.first_name")
    last_name=serializers.CharField(source='user.last_name')
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = Patient
        fields = [
            "id","first_name","last_name", "username", "email", "password",
             "age","gender"
        ]
        read_only_fields = ["id", "created_at"]

    def create(self, validated_data):
        # extract user-related fields
        first_name = validated_data.pop("user", {}).get("first_name", "")
        last_name = validated_data.pop("user", {}).get("last_name", "")
        username = validated_data.pop("username")
        
        email = validated_data.pop("email")
        password = validated_data.pop("password")

        # create user
        user = CustomUser.objects.create_user(
            first_name=first_name,last_name=last_name,username=username, email=email, password=password ,is_active=False
        )

        # create doctor profile with is_verified default=False
        patient = Patient.objects.create(user=user, **validated_data)

        return patient
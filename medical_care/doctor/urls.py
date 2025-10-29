from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import DoctorRegisterView,DoctorViewSet

router=DefaultRouter()

router.register("register",DoctorRegisterView,basename='doctor_register')
router.register("view",DoctorViewSet,basename="doctor")

urlpatterns = [
    path("",include(router.urls))
]

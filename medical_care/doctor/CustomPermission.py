from rest_framework.permissions import BasePermission

class DoctorPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        elif request.method == 'POST' or request.POST == 'PUT' or request.method == 'PATCH':
            if request.user.is_superuser:
                return True
            return False
        return False
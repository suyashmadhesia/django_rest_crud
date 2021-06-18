from rest_framework.permissions import BasePermission


# this custom permission class in django creating custom permissions for user
# like here we are doing if request.method has get request then only we grant permissions

class MyPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        else:
            return False

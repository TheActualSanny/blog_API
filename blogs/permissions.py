from rest_framework.permissions import BasePermission, SAFE_METHODS

class CreateIfAuthenticated(BasePermission):
    '''
        If the request type is in SAFE_METHODS, ( If it is a GET, HEAD or OPTIONS request )
        it returns True. If it isn't, it checks if the right user is authenticated or not.
    '''
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user
    
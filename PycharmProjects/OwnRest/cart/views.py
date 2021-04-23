from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Cart
from .serializers import CartSerializer
from .permissions import IsAuthorPermission

class PermissionMixin:
    def get_permissions(self):
        if self.action == 'create':
            permissions = [IsAuthenticated, ]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsAuthorPermission, IsAuthenticated]
        else:
            permissions = []
        return [permission() for permission in permissions]

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}


class CartViewSet(PermissionMixin, viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        from account.models import MyUser

        qs = self.request.user
        queryset = super().get_queryset()
        queryset = queryset.filter(user=qs)
        return queryset
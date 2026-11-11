from rest_framework import mixins, permissions, viewsets

from .models import Ticket
from .serializers import TicketSerializer, TicketStaffSerializer


class PeutModifierSiPersonnel(permissions.BasePermission):
    """Connecté pour lister, lire et créer ; personnel pour modifier."""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.method in ("PUT", "PATCH"):
            return request.user.is_staff
        return True


class TicketViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [PeutModifierSiPersonnel]
    http_method_names = ["get", "post", "patch", "head", "options"]

    def get_serializer_class(self):
        if self.action == "partial_update":
            return TicketStaffSerializer
        return TicketSerializer

    def get_queryset(self):
        return Ticket.objects.select_related("demandeur", "assigne_a").visibles_par(
            self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(demandeur=self.request.user)

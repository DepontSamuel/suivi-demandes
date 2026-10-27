from rest_framework import mixins, viewsets

from .models import Ticket
from .serializers import TicketSerializer


class TicketViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = TicketSerializer

    def get_queryset(self):
        return Ticket.objects.select_related("demandeur", "assigne_a").visibles_par(
            self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(demandeur=self.request.user)
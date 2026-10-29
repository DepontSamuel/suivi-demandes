from rest_framework import serializers

from .models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    demandeur = serializers.StringRelatedField(read_only=True)
    assigne_a = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Ticket
        fields = [
            "id",
            "titre",
            "description",
            "statut",
            "priorite",
            "demandeur",
            "assigne_a",
            "cree_le",
            "modifie_le",
        ]
        read_only_fields = ["statut", "cree_le", "modifie_le"]

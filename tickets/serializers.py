from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Ticket

User = get_user_model()


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


class TicketStaffSerializer(TicketSerializer):
    assigne_a = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_staff=True),
        allow_null=True,
        required=False,
    )

    class Meta(TicketSerializer.Meta):
        read_only_fields = ["titre", "description", "priorite", "cree_le", "modifie_le"]

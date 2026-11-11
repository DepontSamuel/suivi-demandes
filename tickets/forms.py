from django import forms
from django.contrib.auth import get_user_model

from .models import Ticket

User = get_user_model()


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["titre", "description", "priorite"]


class TicketStaffForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["statut", "assigne_a"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["assigne_a"].queryset = User.objects.filter(is_staff=True)

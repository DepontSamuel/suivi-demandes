from django.contrib import admin

from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("titre", "statut", "priorite", "demandeur", "assigne_a", "cree_le")
    list_filter = ("statut", "priorite")
    search_fields = ("titre", "description")
from django.conf import settings
from django.db import models

class TicketQuerySet(models.QuerySet):
    def visibles_par(self, user):
        """Tickets qu'un utilisateur a le droit de voir."""
        if user.is_staff:
            return self
        return self.filter(demandeur=user)

class Ticket(models.Model):
    objects = TicketQuerySet.as_manager()

    class Statut(models.TextChoices):
        OUVERT = "ouvert", "Ouvert"
        EN_COURS = "en_cours", "En cours"
        RESOLU = "resolu", "Résolu"

    class Priorite(models.TextChoices):
        BASSE = "basse", "Basse"
        NORMALE = "normale", "Normale"
        HAUTE = "haute", "Haute"

    titre = models.CharField(max_length=200)
    description = models.TextField()
    statut = models.CharField(
        max_length=20, choices=Statut.choices, default=Statut.OUVERT
    )
    priorite = models.CharField(
        max_length=20, choices=Priorite.choices, default=Priorite.NORMALE
    )
    demandeur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="tickets_crees",
    )
    assigne_a = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tickets_assignes",
    )
    cree_le = models.DateTimeField(auto_now_add=True)
    modifie_le = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-cree_le"]

    def __str__(self):
        return f"#{self.pk} {self.titre}"
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase

from .models import Ticket

User = get_user_model()


class TicketApiTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.agent1 = User.objects.create_user("agent1", password="mdp-test-123")
        cls.agent2 = User.objects.create_user("agent2", password="mdp-test-123")
        cls.ticket1 = Ticket.objects.create(
            titre="Ticket agent1", description="Texte", demandeur=cls.agent1
        )
        cls.ticket2 = Ticket.objects.create(
            titre="Ticket agent2", description="Texte", demandeur=cls.agent2
        )

    def test_anonyme_refuse(self):
        response = self.client.get(reverse("ticket-list"))
        self.assertIn(response.status_code, (401, 403))

    def test_agent_liste_ses_tickets(self):
        self.client.force_authenticate(self.agent1)
        response = self.client.get(reverse("ticket-list"))
        self.assertEqual(response.status_code, 200)
        titres = [t["titre"] for t in response.data["results"]]
        self.assertEqual(titres, ["Ticket agent1"])

    def test_detail_du_ticket_d_un_autre_agent_est_404(self):
        self.client.force_authenticate(self.agent1)
        response = self.client.get(reverse("ticket-detail", args=[self.ticket2.pk]))
        self.assertEqual(response.status_code, 404)

    def test_creation_ignore_les_champs_proteges(self):
        self.client.force_authenticate(self.agent1)
        response = self.client.post(
            reverse("ticket-list"),
            {
                "titre": "Via API",
                "description": "Texte",
                "priorite": "haute",
                "statut": "resolu",
                "demandeur": self.agent2.pk,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        ticket = Ticket.objects.get(titre="Via API")
        self.assertEqual(ticket.demandeur, self.agent1)
        self.assertEqual(ticket.statut, Ticket.Statut.OUVERT)

    def test_creation_invalide_renvoie_400(self):
        self.client.force_authenticate(self.agent1)
        response = self.client.post(
            reverse("ticket-list"), {"titre": "", "description": "x"}, format="json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("titre", response.data)

    def test_suppression_non_autorisee(self):
        self.client.force_authenticate(self.agent1)
        response = self.client.delete(reverse("ticket-detail", args=[self.ticket1.pk]))
        self.assertEqual(response.status_code, 405)

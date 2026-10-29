from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Ticket

User = get_user_model()


class TicketModelTests(TestCase):
    def test_valeurs_par_defaut(self):
        user = User.objects.create_user("agent", password="mdp-test-123")
        ticket = Ticket.objects.create(titre="Imprimante", description="En panne", demandeur=user)
        self.assertEqual(ticket.statut, Ticket.Statut.OUVERT)
        self.assertEqual(ticket.priorite, Ticket.Priorite.NORMALE)
        self.assertIsNone(ticket.assigne_a)

    def test_representation_texte(self):
        user = User.objects.create_user("agent", password="mdp-test-123")
        ticket = Ticket.objects.create(titre="Imprimante", description="En panne", demandeur=user)
        self.assertEqual(str(ticket), f"#{ticket.pk} Imprimante")


class TicketViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.agent1 = User.objects.create_user("agent1", password="mdp-test-123")
        cls.agent2 = User.objects.create_user("agent2", password="mdp-test-123")
        cls.support = User.objects.create_user("support", password="mdp-test-123", is_staff=True)
        cls.ticket1 = Ticket.objects.create(
            titre="Ticket agent1", description="Texte", demandeur=cls.agent1
        )
        cls.ticket2 = Ticket.objects.create(
            titre="Ticket agent2", description="Texte", demandeur=cls.agent2
        )

    def test_liste_redirige_si_anonyme(self):
        url = reverse("tickets:liste")
        response = self.client.get(url)
        self.assertRedirects(response, f"{reverse('login')}?next={url}")

    def test_agent_ne_voit_que_ses_tickets(self):
        self.client.force_login(self.agent1)
        response = self.client.get(reverse("tickets:liste"))
        self.assertContains(response, "Ticket agent1")
        self.assertNotContains(response, "Ticket agent2")

    def test_personnel_voit_tous_les_tickets(self):
        self.client.force_login(self.support)
        response = self.client.get(reverse("tickets:liste"))
        self.assertContains(response, "Ticket agent1")
        self.assertContains(response, "Ticket agent2")

    def test_detail_de_son_ticket(self):
        self.client.force_login(self.agent1)
        response = self.client.get(reverse("tickets:detail", args=[self.ticket1.pk]))
        self.assertEqual(response.status_code, 200)

    def test_detail_du_ticket_d_un_autre_agent_est_404(self):
        self.client.force_login(self.agent1)
        response = self.client.get(reverse("tickets:detail", args=[self.ticket2.pk]))
        self.assertEqual(response.status_code, 404)

    def test_creation_fixe_le_demandeur_cote_serveur(self):
        self.client.force_login(self.agent1)
        response = self.client.post(
            reverse("tickets:creer"),
            {
                "titre": "Nouveau",
                "description": "Texte",
                "priorite": "haute",
                # champs que l'utilisateur ne doit pas pouvoir imposer :
                "demandeur": self.agent2.pk,
                "statut": "resolu",
            },
        )
        self.assertRedirects(response, reverse("tickets:liste"))
        ticket = Ticket.objects.get(titre="Nouveau")
        self.assertEqual(ticket.demandeur, self.agent1)
        self.assertEqual(ticket.statut, Ticket.Statut.OUVERT)

    def test_creation_sans_titre_est_refusee(self):
        self.client.force_login(self.agent1)
        nb_avant = Ticket.objects.count()
        response = self.client.post(
            reverse("tickets:creer"),
            {"titre": "", "description": "Texte", "priorite": "basse"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("titre", response.context["form"].errors)
        self.assertEqual(Ticket.objects.count(), nb_avant)

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import TicketForm, TicketStaffForm
from .models import Ticket


class TicketQuerysetMixin(LoginRequiredMixin):
    """Un agent ne voit que ses demandes ; le personnel du service voit tout."""

    def get_queryset(self):
        return Ticket.objects.select_related("demandeur", "assigne_a").visibles_par(
            self.request.user
        )


class TicketListView(TicketQuerysetMixin, ListView):
    model = Ticket
    paginate_by = 20


class TicketDetailView(TicketQuerysetMixin, DetailView):
    model = Ticket


class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    form_class = TicketForm
    success_url = reverse_lazy("tickets:liste")

    def form_valid(self, form):
        form.instance.demandeur = self.request.user
        return super().form_valid(form)


class TicketUpdateView(UserPassesTestMixin, UpdateView):
    model = Ticket
    form_class = TicketStaffForm
    template_name = "tickets/ticket_update.html"

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse("tickets:detail", kwargs={"pk": self.object.pk})

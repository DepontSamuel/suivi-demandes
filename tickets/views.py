from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from .forms import TicketForm
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

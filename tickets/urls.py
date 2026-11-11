from django.urls import path

from . import views

app_name = "tickets"

urlpatterns = [
    path("", views.TicketListView.as_view(), name="liste"),
    path("nouveau/", views.TicketCreateView.as_view(), name="creer"),
    path("<int:pk>/", views.TicketDetailView.as_view(), name="detail"),
    path("<int:pk>/modifier/", views.TicketUpdateView.as_view(), name="modifier"),
]

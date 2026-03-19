from django.urls import path
from .views import TicketListCreateView, TicketDetailView, TicketTrackingView

urlpatterns = [
    path('', TicketListCreateView.as_view(), name='ticket-list-create'),
    path('track/', TicketTrackingView.as_view(), name='ticket-track'),
    path('<str:ulid>/', TicketDetailView.as_view(), name='ticket-detail'),
]
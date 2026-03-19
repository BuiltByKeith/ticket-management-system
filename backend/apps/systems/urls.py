from django.urls import path
from .views import SystemListCreateView, SystemDetailView

urlpatterns = [
    path("", SystemListCreateView.as_view(), name="system-list-create"),
    path("<str:ulid>/", SystemDetailView.as_view(), name="system-detail"),
]

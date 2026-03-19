from django.urls import path
from .views import OfficeListCreateView, OfficeDetailView

urlpatterns = [
    path("", OfficeListCreateView.as_view(), name="office-list-create"),
    path("<str:ulid>/", OfficeDetailView.as_view(), name="office-detail"),
]

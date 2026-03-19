from django.urls import path
from .views import ConcernTypeListCreateView, ConcernTypeDetailView

urlpatterns = [
    path('', ConcernTypeListCreateView.as_view(), name='concern-type-list-create'),
    path('<str:ulid>/', ConcernTypeDetailView.as_view(), name='concern-type-detail'),
]
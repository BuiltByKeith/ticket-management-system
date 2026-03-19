from django.urls import path, include

urlpatterns = [
    path('auth/', include('apps.users.urls')),
    path('users/', include('apps.users.urls_users')),
    path('offices/', include('apps.offices.urls')),
    path('systems/', include('apps.systems.urls')),
    path('concern-types/', include('apps.concern_types.urls')),
    path('tickets/', include('apps.tickets.urls')),
]
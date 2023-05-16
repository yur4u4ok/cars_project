from django.urls import path, include


urlpatterns = [
    path('auth', include('apps.auth.urls')),
    path('users', include('apps.users.urls')),
    path('adverts', include('apps.advertisements.urls')),
]

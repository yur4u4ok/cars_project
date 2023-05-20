from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.permissions import AllowAny

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title='AutoRiaCloneAPI',
        default_version='v1',
        description='About the sale of cars',
        contact=openapi.Contact(email='ostap4uk43yurchuk@gmail.com')
    ),
    public=True,
    permission_classes=[AllowAny]
)

urlpatterns = [
    path('auth', include('apps.auth.urls')),
    path('users', include('apps.users.urls')),
    path('adverts', include('apps.advertisements.urls')),
    path('doc', schema_view.with_ui('swagger', cache_timeout=0)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

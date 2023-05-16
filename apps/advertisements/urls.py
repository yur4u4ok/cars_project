from django.urls import path

from .views import ListAllAdvertsView, CreateAdvertisementView, ActivateAdvert


urlpatterns = [
    path('', ListAllAdvertsView.as_view(), name='list_all_adverts'),
    path('/create', CreateAdvertisementView.as_view(), name='create_advert'),
    path('/<int:pk>/update', ActivateAdvert.as_view(), name='activate_advert'),
]

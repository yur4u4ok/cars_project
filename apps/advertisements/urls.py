from django.urls import path

from .views import ListAllAdvertsView, ListCreateAdvertsView, \
    UpdateAdvertView, ActivateAdvertView, ApproveSuspiciousAdvertsView, DestroyInvalidAdvertView, \
    ListSuspiciousAdvertsView, GetAdvertView, DeactivateAdvertView, AdvertAddPhotoView, \
    AdvertDeletePhotoView, DeleteAdvertView

urlpatterns = [
    path('', ListAllAdvertsView.as_view(), name='list_all_adverts'),
    path('/<int:pk>', GetAdvertView.as_view(), name='get_advert'),

    # FOR LOGINED USER
    path('/mine', ListCreateAdvertsView.as_view(), name='list_create_advert'),
    path('/<int:pk>/update', UpdateAdvertView.as_view(), name='update_advert'),
    path('/<int:pk>/delete', DeleteAdvertView.as_view(), name='delete_advert'),
    path('/<int:pk>/photo', AdvertAddPhotoView.as_view(), name='add_photo'),
    path('/<int:pk>/delete_photo', AdvertDeletePhotoView.as_view(), name='delete_photo'),
    path('/<int:pk>/activate', ActivateAdvertView.as_view(), name='activate_advert'),
    path('/<int:pk>/deactivate', DeactivateAdvertView.as_view(), name='deactivate_advert'),

    # FOR MANAGER
    path('/suspicious', ListSuspiciousAdvertsView.as_view(), name='list_suspicious_adverts'),
    path('/<int:pk>/approve', ApproveSuspiciousAdvertsView.as_view(), name='approve_suspicious_adverts'),
    path('/<int:pk>/destroy', DestroyInvalidAdvertView.as_view(), name='destroy_adverts'),
]

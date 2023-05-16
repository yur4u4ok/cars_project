from django.urls import path

from .views import UserToManagerView, ManagerToUserView, ManagerBlockView, \
    ManagerUnBlockView, GetAllUsersView, UserBlockView, UserUnBlockView

urlpatterns = [
    # FOR SUPERUSER
    path('/<int:pk>/to_manager', UserToManagerView.as_view(), name='user_to_manager'),
    path('/<int:pk>/to_user', ManagerToUserView.as_view(), name='manager_to_user'),
    path('/<int:pk>/block_manager', ManagerBlockView.as_view(), name='block_manager'),
    path('/<int:pk>/unblock_manager', ManagerUnBlockView.as_view(), name='unblock_manager'),

    # FOR MANAGER
    path('', GetAllUsersView.as_view(), name='get_all_users'),
    path('<int:pk>/block', UserBlockView.as_view(), name='block_user'),
    path('<int:pk>/unblock', UserUnBlockView.as_view(), name='unblock_user'),
]

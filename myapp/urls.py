
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    register_user,
    user_login,
    create_task,
    read_task,
    update_task,
    delete_task,
    add_task_member,
    remove_task_member,
    update_task_status
)

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', user_login, name='login'),
    path('tasks/', create_task, name='create_task'),
    path('tasks/<int:task_id>/', read_task, name='read_task'),
    path('tasks/<int:task_id>/update/', update_task, name='update_task'),
    path('tasks/<int:task_id>/delete/', delete_task, name='delete_task'),
    path('tasks/<int:task_id>/add_member/<int:user_id>/', add_task_member, name='add_task_member'),
    path('tasks/<int:task_id>/remove_member/<int:user_id>/', remove_task_member, name='remove_task_member'),
    path('tasks/<int:task_id>/update_status/', update_task_status, name='update_task_status'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
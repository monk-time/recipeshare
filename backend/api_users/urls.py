from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet

app_name = 'api_users'

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='user')

unneccesary_djoser_path_names = [
    'user-activation',
    'user-resend-activation',
    'user-reset-username',
    'user-reset-username-confirm',
    'user-reset-password',
    'user-reset-password-confirm',
    'user-set-username',
]


router_v1_filtered = [
    url
    for url in router_v1.urls
    if url.name not in unneccesary_djoser_path_names
]

urlpatterns = [
    path('', include(router_v1_filtered)),
    path('auth/', include('djoser.urls.authtoken')),
]

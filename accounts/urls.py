from django.conf.urls import url
from accounts import views
from rest_framework.authtoken import views as authviews

urlpatterns = [
    url(r'api-token-auth', authviews.obtain_auth_token),
    url(r'create', views.user_create),
    url(r'delete', views.user_delete),
    url(r'get', views.user_get_all),
]

from django.conf.urls import url
from django.urls import include, path
from rest_framework import routers

from .views import RegisterView, ConfirmEmailView, ResetPasswordView, LogoutView, UserViewSet

authpatterns = [
    url(r'^register/', RegisterView.as_view(), name='register'),
    url(r'^confirm/', ConfirmEmailView.as_view(), name='confirm'),
    url(r'^reset/', ResetPasswordView.as_view(), name='reset'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),
]

router = routers.DefaultRouter()
router.register('user', UserViewSet)
urlpatterns = [
    path('auth/', include(authpatterns)),
] + router.urls
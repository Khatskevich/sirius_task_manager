from django.conf.urls import url
from .views import RegisterView, ConfirmEmailView, ResetPasswordView, LogoutView

urlpatterns = [
    url(r'^register/', RegisterView.as_view(), name='register'),
    url(r'^confirm/', ConfirmEmailView.as_view(), name='confirm'),
    url(r'^reset/', ResetPasswordView.as_view(), name='reset'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),
]
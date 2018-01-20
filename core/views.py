from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout, get_user_model
from django.utils.translation import ugettext_lazy as _

from rest_framework import status, viewsets, permissions, mixins
from rest_framework.decorators import detail_route
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import User
from .serializers import RegistrationSerializer, ShortUserInfoSerializer, \
    ValidationCodeSerializer, ResetPasswordSerializer, UserSerializer
from .tasks import send_reset_password_email


UserModel = get_user_model()


class BaseAuthView(APIView):
    permission_classes = ()
    authentication_classes = ()

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
            'view': self,
        }

    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        Defaults to using `self.serializer_class`.
        You may want to override this if you need to provide different
        serializations depending on the incoming request.
        (Eg. admins get full serialization, others get basic serialization)
        """
        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method."
            % self.__class__.__name__)
        return self.serializer_class

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)


class RegisterView(BaseAuthView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        # user = serializer.object.get('user') or request.user
        user = UserModel.objects.create_user(
            email=serializer.object.get('email'),
            password=serializer.object.get('password'),
            first_name=serializer.object.get('first_name'),
            last_name=serializer.object.get('last_name')
        )
        if not user:
            return Response({'status': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"status": True, 'messages': {'non_field': _("You was registered.")}})


class ConfirmEmailView(BaseAuthView):
    serializer_class = ValidationCodeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = serializer.object.get('user')
        user.is_valid = True
        user.save()
        return Response({'status': True, 'messages': {'non_field': _("Email validation success")}})


class ResetPasswordView(BaseAuthView):
    serializer_class = ResetPasswordSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            pass
        else:
            user = serializer.validated_data.get('user')
            password = UserModel.objects.make_random_password()
            send_reset_password_email.apply_async(kwargs={'email': user.email, 'password': password})
            user.set_password(password)
            user.save()
            serializer.save()
        return Response({'status': True, 'messages': {'non_field': _("New password was sent on your email.")}})


class UserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer
    pagination_class = None
    queryset = User.objects.all()

    @detail_route(methods=['post'])
    def subscribe(self, request, pk):
        user = self.get_object()
        if user.pk == request.user.pk:
            return Response(_("You cannot subscribe on yourself"), status=status.HTTP_400_BAD_REQUEST)
        request.user.subscribed_on.add(user)
        return Response("")

    @detail_route(methods=['post'])
    def unsubscribe(self, request, pk):
        user = self.get_object()
        request.user.subscribed_on.remove(user)
        return Response("")


class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    def post(self, request):
        logout(request)
        return redirect("index")

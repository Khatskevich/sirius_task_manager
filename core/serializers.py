from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.core import exceptions
from django.utils.translation import ugettext as _
from rest_framework import serializers
from .models import ValidationCode, ResetPassword
import django.contrib.auth.password_validation as validators

USER_MODEL = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER_MODEL
        fields = ('email', 'last_name', 'first_name')


class PasswordField(serializers.CharField):

    def __init__(self, *args, **kwargs):
        if 'style' not in kwargs:
            kwargs['style'] = {'input_type': 'password'}
        else:
            kwargs['style']['input_type'] = 'password'
        super(PasswordField, self).__init__(*args, **kwargs)


def get_username_field():
    try:
        username_field = get_user_model().USERNAME_FIELD
    except:
        username_field = 'username'

    return username_field


def get_username(user):
    try:
        username = user.get_username()
    except AttributeError:
        username = user.username

    return username


# TODO: Добавить больше валидации
class RegistrationSerializer(serializers.ModelSerializer):
    password1 = PasswordField(write_only=True)
    password2 = PasswordField(write_only=True)

    @property
    def object(self):
        return self.validated_data

    class Meta:
        model = USER_MODEL
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def validate(self, attrs):
        credentials = {
            'email': attrs.get('email'),
            'password': attrs.get('password1'),
            'first_name': attrs.get('first_name'),
            'last_name': attrs.get('last_name'),
        }

        if not all(credentials.values()):
            msg = _('Must include "{username_field}" and "password".')
            msg = msg.format(username_field="email")
            raise serializers.ValidationError(msg)

        pass1 = attrs.get('password1')
        pass2 = attrs.get('password2')

        if pass1 != pass2:
            msg = _('Passwords are not equal!')
            raise serializers.ValidationError(msg)

        errors = dict()
        try:
            validators.validate_password(password=pass1, user=USER_MODEL)

        except exceptions.ValidationError as e:
            errors['password1'] = list(e.messages)
            raise serializers.ValidationError(errors)

        return credentials


class ShortUserInfoSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField(read_only=True)
    is_authenticated = serializers.SerializerMethodField(read_only=True)
    rating = serializers.SerializerMethodField(read_only=True, required=False)

    class Meta:
        model = USER_MODEL
        fields = ('id', 'is_authenticated', 'email', 'permissions', 'rating')
        extra = {'is_authenticated': {'read_only': True},
                 'id': {'read_only': True}
                 }

    def get_permissions(self, obj):
        return obj.get_all_permissions()

    def get_is_authenticated(self, obj):
        return obj.is_authenticated()

    def get_rating(self, obj):
        if obj.rating:
            return obj.rating.is_good
        return None


class ValidationCodeSerializer(serializers.ModelSerializer):
    code = serializers.UUIDField()

    class Meta:
        model = ValidationCode
        fields = ('code',)

    @property
    def object(self):
        return self.validated_data

    def validate(self, attrs):
        code = attrs.get('code', None)
        if code is None:
            msg = _('Invalid validation code')
            raise serializers.ValidationError(msg)
        try:
            user = USER_MODEL.objects.filter(validation_code__code=code).get()
        except USER_MODEL.DoesNotExist:
            msg = _('Invalid validation code')
            raise serializers.ValidationError(msg)

        return {
            'user': user
        }


class ResetPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = ResetPassword
        fields = ('email', )

    def validate(self, attrs):
        email = attrs.get('email', None)
        try:
            user = USER_MODEL.objects.get(email=email)
        except USER_MODEL.DoesNotExist:
            msg = _('User with this email not found')
            raise serializers.ValidationError(msg)

        return {
            'user': user
        }
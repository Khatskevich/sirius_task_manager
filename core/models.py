import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_valid', False)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_valid', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ()
    username = None
    email = models.EmailField(_('email address'), blank=False, unique=True)
    is_valid = models.BooleanField(_('is valid'), blank=False, default=False)
    subscribed_on = models.ManyToManyField("self", related_name='subscribers', blank=True)
    objects = UserManager()


class ValidationCode(models.Model):
    user = models.OneToOneField(User, verbose_name=_('user'), related_name='validation_code', on_delete=models.CASCADE)
    code = models.UUIDField(verbose_name=_('validation code'), default=uuid.uuid4, editable=False)


class ResetPassword(models.Model):
    user = models.ForeignKey(User, verbose_name=_('user'), related_name='+', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))

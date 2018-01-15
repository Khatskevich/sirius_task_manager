from django.db.models.signals import post_save
from .models import User, ValidationCode
from .mail import RegistrationMessage
# from .tasks import send_registration_email


# def onUserCreationValidationCodeSend(sender, instance, created, **kwargs):
#     if created:
#         validation_code = ValidationCode.objects.create(user=instance)
#         send_registration_email.apply_async((instance.email, validation_code.code))
#
#
# post_save.connect(onUserCreationValidationCodeSend, sender=User)

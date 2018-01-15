from django.core.mail import EmailMessage
from django.utils.translation import ugettext_lazy as _
from sirius_task_manager.settings import SITE_ADDRESS


class RegistrationMessage(EmailMessage):
    def __init__(self, code, to):
        body = self.get_reg_body(code)
        super().__init__(subject="Registration message", body=self.get_reg_body(code), to=[to, ])

    def get_reg_body(self, code):
        site_addr = SITE_ADDRESS + "/login/activate?code=" + str(code)
        return "To activate your account visit this link: " + site_addr


class ResetPasswordMessage(EmailMessage):
    def __init__(self, password, to):
        super().__init__(subject="Reset password", body=self.get_reset_body(password), to=[to, ])

    def get_reset_body(self, password):
        site_addr = SITE_ADDRESS + "/login"
        return "Your password was changed.\nNew password: %s .\nLogin link: %s" % (password, site_addr)

from sirius_task_manager.celery import app
from .mail import RegistrationMessage, ResetPasswordMessage


# @app.task(bind=True)
# def send_registration_email(self, email, code):
#     RegistrationMessage(to=email, code=code).send()


@app.task()
def send_reset_password_email(email, password):
    ResetPasswordMessage(to=email, password=password).send()

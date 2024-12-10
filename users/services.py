from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string




class SendEmail:
    @staticmethod
    def send_confirmation_email(email, otp_code):
        subject = 'Welcome to my Service'
        message = render_to_string("index.html", context={
            "email": email,
            "otp_code": otp_code
        })
        email = EmailMessage(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email]
        )
        email.content_subtype = "html"
        email.send(fail_silently=False)




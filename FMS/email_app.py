from django.conf import settings
from django.core.mail import send_mail

def sendEmail(context, extras):
    try:
        settings.EMAIL_HOST = 'mail.startall.net'
        settings.EMAIL_PORT = 465
        settings.EMAIL_HOST_USER = 'passwordreset@startall.net'
        settings.EMAIL_HOST_PASSWORD = 'j5hBhD[[kTCT'
        unknown_user = context.user
        
        send_mail(
            f"Unauthorized Access!",
            f"Click the link to give {unknown_user} access to your file {(extras if extras != None else context.user)}",
            "noreply@emailmgt.com",
            ["richiedilosi2003@gmail.com"],
            fail_silently=False,
        )
        return "sent"
    except Exception as e:
        return "Not Successfull"
from django.core.mail import EmailMessage
# from config.celery import app


# @app.task(ignore_result=True)
def send_mail(data):
    email = EmailMessage(
        subject="Beam",
        body=data['email_body'],
        to=[data['to_email']]
    )
    email.content_subtype = "html"
    email.send()
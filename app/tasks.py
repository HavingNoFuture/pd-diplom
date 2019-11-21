from django.conf import settings
from django.core.mail import send_mail

from orders.celery import app


@app.task
def send_registration_mail(to_user_email):
    send_mail(
        subject='Registration on best shop',
        message='Hello! My dear friend!',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[to_user_email,],
        fail_silently=False,
    )

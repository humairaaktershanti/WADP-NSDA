from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings


def sentMailPage(request):
    user_email = 'cset-210608@dti.ac'
    send_mail(
        'practice Email sent',
        'mail check habib',
        settings.EMAIL_HOST_USER,
        [user_email]
    )

    return render(request,"sent_mail.html")


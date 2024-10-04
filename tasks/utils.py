from rest_framework import serializers
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings


def check_datetime(value):
    if value < timezone.now():
        raise serializers.ValidationError("la date ne doit pas etre dans le passe")
    return value


def send_activation_email(user):
    subject = "Activation de votre compte"
    uid = urlsafe_base64_encode(force_bytes(user.id))
    token = default_token_generator.make_token(user)
    message = render_to_string(
        'registration/activation_email.html', {
            'user': user,
            'uid': uid,
            'token': token,
            'domain': settings.DOMAIN_URL
        }
    )
    send_mail(
        subject, message,
        'backend@nimbasms.com',
        [user.email],
        fail_silently=True
    )

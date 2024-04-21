from django.contrib.auth.models import User, AbstractUser
from django.db import models

# Create your models here.
from django.db.models import SET_NULL
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class UserModel(User):
    avatar = models.ImageField(upload_to='uploads/', blank=True)
    phone_num = models.CharField(max_length=20)
    password1 = models.CharField(max_length=100)
    password2 = models.CharField(max_length=100)


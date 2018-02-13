from __future__ import unicode_literals
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have a valid e-mail address')

        if not username:
            raise ValueError('Users must have a valid username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=kwargs.get('first_name'),
            last_name=kwargs.get('last_name'),
            birth_date=kwargs.get('birth_date', None),
            country=kwargs.get('country', None),
            gender=kwargs.get('gender', None),
        )

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password=None, **kwargs):
        user = self.create_user(username, email, password, **kwargs)

        user.is_admin = True
        user.save()

        return user


class User(AbstractBaseUser):
    username = models.CharField(unique=True, max_length=50)
    email = models.EmailField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(choices=[('M', 'Male',), ('F', 'Female',)], max_length=1, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def get_full_name(self):
        return ' '.join(self.first_name, self.last_login)


class Location(models.Model):
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=2500)


class Visit(models.Model):
    user_id = models.ForeignKey('User')
    location_id = models.ForeignKey('Location')
    date = models.DateTimeField(auto_now=True)
    ratio = models.IntegerField(choices=((str(x), x) for x in range(10)))

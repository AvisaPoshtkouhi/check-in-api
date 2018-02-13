# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from rest_framework_jwt import utils

from snippets.models import User


class JWTAuthTestCase(TestCase):
    token = ''

    def setUp(self):
        self.user_dict = {
            "username": "ivan29",
            "password": "password123",
            "confirm_password": "password123",
            "first_name": "Ivan",
            "last_name": "Ivanov",
            "email": "ivanov@mail.com",
            "birth_date": "1991-01-04",
            "country": "Russia",
            "gender": "M"
        }

        self.user = User.objects.create_user(**self.user_dict)

        jwt_payload_handler = utils.jwt_payload_handler
        jwt_encode_handler = utils.jwt_encode_handler

        payload = jwt_payload_handler(self.user)
        self.token = jwt_encode_handler(payload)

    def getJWTToken(self):
        return 'JWT {}'.format(self.token)

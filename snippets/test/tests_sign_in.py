# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.test import TestCase

from snippets.models import User


class SignInAPITest(TestCase):

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

        self.username = self.user_dict["username"]
        self.email = self.user_dict["email"]
        self.password = self.user_dict["password"]
        first_name = self.user_dict["first_name"]
        last_name = self.user_dict["last_name"]
        self.user = User.objects.create_user(self.username, self.email, self.password, first_name=first_name,
                                             last_name=last_name)

    def test_sign_in(self):
        response = self.client.post('/sign_in',
                                    json.dumps(self.user_dict),
                                    content_type="application/json")

        response_content = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200, response_content)
        self.assertEqual(response_content["status"], "Successful")
        self.assertIsNotNone(response_content['token'])

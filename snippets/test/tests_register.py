# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.test import TestCase


class RegisterAPITest(TestCase):
    user_dict = {
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

    def test_register(self):
        response = self.client.post('/register',
                                    json.dumps(self.user_dict),
                                    content_type="application/json")

        response_content = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 201)

        self.assertEqual(response_content["username"], self.user_dict["username"])
        self.assertEqual(response_content["first_name"], self.user_dict["first_name"])
        self.assertEqual(response_content["last_name"], self.user_dict["last_name"])
        self.assertEqual(response_content["email"], self.user_dict["email"])
        self.assertEqual(response_content["birth_date"], self.user_dict["birth_date"])
        self.assertEqual(response_content["country"], self.user_dict["country"])
        self.assertEqual(response_content["gender"], self.user_dict["gender"])
        self.assertEqual(response_content["id"], 1)

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from .jwt_auth_testcase import JWTAuthTestCase
from snippets.models import Location, Visit
from datetime import datetime


class UserAPITest(JWTAuthTestCase):

    def setUp(self):
        JWTAuthTestCase.setUp(self)

    def test_get_all_user(self):
        response = self.client.get("/users", {}, content_type="application/json",
                                   HTTP_AUTHORIZATION=self.getJWTToken())

        response_content = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200, response_content)
        self.assertEqual(response_content[0]["username"], self.user_dict["username"])
        self.assertEqual(response_content[0]["first_name"], self.user_dict["first_name"])
        self.assertEqual(response_content[0]["last_name"], self.user_dict["last_name"])
        self.assertEqual(response_content[0]["email"], self.user_dict["email"])
        self.assertEqual(response_content[0]["birth_date"], self.user_dict["birth_date"])
        self.assertEqual(response_content[0]["country"], self.user_dict["country"])
        self.assertEqual(response_content[0]["gender"], self.user_dict["gender"])
        self.assertEqual(response_content[0]["id"], 1)

    def test_get_user_by_id(self):
        response = self.client.get("/users/1", {}, content_type="application/json",
                                   HTTP_AUTHORIZATION=self.getJWTToken())

        response_content = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200, response_content)

        self.assertEqual(response.status_code, 200, response_content)
        self.assertEqual(response_content["username"], self.user_dict["username"])
        self.assertEqual(response_content["first_name"], self.user_dict["first_name"])
        self.assertEqual(response_content["last_name"], self.user_dict["last_name"])
        self.assertEqual(response_content["email"], self.user_dict["email"])
        self.assertEqual(response_content["birth_date"], self.user_dict["birth_date"])
        self.assertEqual(response_content["country"], self.user_dict["country"])
        self.assertEqual(response_content["gender"], self.user_dict["gender"])
        self.assertEqual(response_content["id"], 1)

    def test_put_location(self):
        new_user_dict = {
            "username": "USA",
            "first_name": "NewFirstName",
            "last_name": "NewLastName",
            "email": "newemail@gmail.com",
            "birth_date": "1967-02-01",
            "country": "USA",
            "gender": "F",
            "password": "password123",
            "confirm_password": "password123",
        }
        response = self.client.put("/users/1", json.dumps(new_user_dict), content_type="application/json",
                                   HTTP_AUTHORIZATION=self.getJWTToken())

        response_content = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200, response_content)

        self.assertEqual(response_content["username"], new_user_dict["username"])
        self.assertEqual(response_content["first_name"], new_user_dict["first_name"])
        self.assertEqual(response_content["last_name"], new_user_dict["last_name"])
        self.assertEqual(response_content["email"], new_user_dict["email"])
        self.assertEqual(response_content["birth_date"], new_user_dict["birth_date"])
        self.assertEqual(response_content["country"], new_user_dict["country"])
        self.assertEqual(response_content["gender"], new_user_dict["gender"])
        self.assertEqual(response_content["id"], 1)

    def test_delete_user(self):
        response = self.client.delete("/users/1", content_type="application/json",
                                      HTTP_AUTHORIZATION=self.getJWTToken())
        self.assertEqual(response.status_code, 204)

    def test_get_ration_from_user(self):
        location_dict1 = {
            "country": "Russia",
            "city": "Perm",
            "name": "Kama river",
            "description": "Very beautiful place"
        }

        location_dict2 = {
            "country": "Russia",
            "city": "Moscow",
            "name": "Kama river",
            "description": "Very beautiful place"
        }

        location1 = Location.objects.create(**location_dict1)
        location2 = Location.objects.create(**location_dict2)

        visit1 = {
            "user_id": self.user,
            "location_id": location1,
            "date": datetime.now(),
            "ratio": "5"
        }

        visit2 = {
            "user_id": self.user,
            "location_id": location2,
            "date": datetime.now(),
            "ratio": "2"
        }

        Visit.objects.create(**visit1)
        Visit.objects.create(**visit2)

        response = self.client.get("/users/1/ratio", {}, content_type="application/json",
                                   HTTP_AUTHORIZATION=self.getJWTToken())

        response_content = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200, response_content)

        self.assertEqual(response_content["count"], 2)
        self.assertEqual(response_content["locations"], [{"id": 1}, {"id": 2}])
        self.assertEqual(response_content["avg"], 3.5)

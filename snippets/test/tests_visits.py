# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from .jwt_auth_testcase import JWTAuthTestCase
from snippets.models import Location, Visit
from datetime import datetime


class VisitAPITest(JWTAuthTestCase):

    def setUp(self):
        JWTAuthTestCase.setUp(self)
        location_dict = {
            "country": "Russia",
            "city": "Perm",
            "name": "Kama river",
            "description": "Very beautiful place"
        }
        self.location = Location.objects.create(**location_dict)

        self.visit = {
            "user_id": self.user,
            "location_id": self.location,
            "date": datetime.now(),
            "ratio": "6"
        }

        Visit.objects.create(**self.visit)

    def test_get_all_visits(self):
        response = self.client.get("/visits", {}, content_type="application/json",
                                   HTTP_AUTHORIZATION=self.getJWTToken())

        response_content = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200, response_content)
        self.assertEqual(response_content[0]["user_id"], self.user.id)
        self.assertEqual(response_content[0]["location_id"], self.location.id)
        self.assertEqual(response_content[0]["ratio"], self.visit["ratio"])
        self.assertEqual(response_content[0]["id"], 1)

    def test_get_visit_by_id(self):
        response = self.client.get("/visits/1", {}, content_type="application/json",
                                   HTTP_AUTHORIZATION=self.getJWTToken())

        response_content = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200, response_content)

        self.assertEqual(response.status_code, 200, response_content)
        self.assertEqual(response_content["user_id"], self.user.id)
        self.assertEqual(response_content["location_id"], self.location.id)
        self.assertEqual(response_content["ratio"], self.visit["ratio"])
        self.assertEqual(response_content["id"], 1)

    def test_put_visit(self):
        new_visit_dict = {
            "user_id": 1,
            "location_id": 1,
            "ratio": "8"
        }

        response = self.client.put("/visits/1", json.dumps(new_visit_dict), content_type="application/json",
                                   HTTP_AUTHORIZATION=self.getJWTToken())

        response_content = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200, response_content)
        self.assertEqual(response_content["ratio"], new_visit_dict["ratio"])
        self.assertEqual(response_content["id"], 1)

    def test_delete_visit(self):
        response = self.client.delete("/visits/1", content_type="application/json",
                                      HTTP_AUTHORIZATION=self.getJWTToken())
        self.assertEqual(response.status_code, 204)

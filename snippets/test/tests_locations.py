# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from .jwt_auth_testcase import JWTAuthTestCase

from snippets.models import Location


class LocationAPITest(JWTAuthTestCase):

    def setUp(self):
        JWTAuthTestCase.setUp(self)
        self.location_dict = {
            "country": "Russia",
            "city": "Perm",
            "name": "Kama river",
            "description": "Very beautiful place"
        }

        Location.objects.create(**self.location_dict)

    def test_get_all_locations(self):
        response = self.client.get("/locations", {}, content_type="application/json",
                                   HTTP_AUTHORIZATION=self.getJWTToken())

        response_content = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200, response_content)

        self.assertEqual(response_content[0]["country"], self.location_dict["country"])
        self.assertEqual(response_content[0]["city"], self.location_dict["city"])
        self.assertEqual(response_content[0]["name"], self.location_dict["name"])
        self.assertEqual(response_content[0]["description"], self.location_dict["description"])
        self.assertEqual(response_content[0]["id"], 1)

    def test_get_location_by_id(self):
        response = self.client.get("/locations/1", {}, content_type="application/json",
                                   HTTP_AUTHORIZATION=self.getJWTToken())

        response_content = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200, response_content)

        self.assertEqual(response_content["country"], self.location_dict["country"])
        self.assertEqual(response_content["city"], self.location_dict["city"])
        self.assertEqual(response_content["name"], self.location_dict["name"])
        self.assertEqual(response_content["description"], self.location_dict["description"])
        self.assertEqual(response_content["id"], 1)

    def test_post_location(self):
        new_location_dict = {
            "country": "USA",
            "city": "New Your",
            "name": "place1",
            "description": "Some place in New Your"
        }
        response = self.client.post("/locations", json.dumps(new_location_dict), content_type="application/json",
                                    HTTP_AUTHORIZATION=self.getJWTToken())

        response_content = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 201)

        self.assertEqual(response_content["country"], new_location_dict["country"])
        self.assertEqual(response_content["city"], new_location_dict["city"])
        self.assertEqual(response_content["name"], new_location_dict["name"])
        self.assertEqual(response_content["description"], new_location_dict["description"])
        self.assertEqual(response_content["id"], 2)

    def test_put_location(self):
        new_location_dict = {
            "country": "USA",
            "city": "New Your",
            "name": "new Name",
            "description": "Some place in New Your"
        }
        response = self.client.put("/locations/1", json.dumps(new_location_dict), content_type="application/json",
                                   HTTP_AUTHORIZATION=self.getJWTToken())

        response_content = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response_content["country"], new_location_dict["country"])
        self.assertEqual(response_content["city"], new_location_dict["city"])
        self.assertEqual(response_content["name"], new_location_dict["name"])
        self.assertEqual(response_content["description"], new_location_dict["description"])
        self.assertEqual(response_content["id"], 1)

    def test_delete_location(self):
        response = self.client.delete("/locations/1", content_type="application/json",
                                      HTTP_AUTHORIZATION=self.getJWTToken())
        self.assertEqual(response.status_code, 204)

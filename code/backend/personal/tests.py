"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from backend.univinfo.models import University
from backend.personal.models import User, UserState

import json
class PersonalTests(APITestCase):
    def setUp(self):
        self.client = Client()
        University.objects.create(id = 1, name = "UCB", shortname="UCB", address="C", numofsemesters=4, description="test")
        university = University.objects.get(id = 1)
        User.objects.create(id = 1,
                            first_name = "er",
                            last_name = "wang",
                            nick_name = "haha",
                            password  = "1111",
                            gender    = "male",
                            image     = "http",
                            eas_id    = "0001",
                            tpa_type  = "1",
                            tpa_id    = "0321",
                            university= university,
                            email     = "abc@132.com",
                            phone     = "112333223"
                            )
        UserState.objects.create(user = User.objects.get(id=1),
                                token = 'test',
                                ip    = '127.0.0.1'
                                )
    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('backend.personal.views.register')
        data = {
                "first_name": "yi",
                "last_name": "chen",
                "nick_name": "hehe",
                "password":"1234",
                "gender": "fmale",
                "image": "http",
                "eas_id": "0001",
                "tpa_type": "1",
                "tpa_id": "lala",
                "university": 1,
                "email": "abc@13.com",
                "phone": "1233211123"
        }
        data = json.dumps(data)
        response = self.client.post(url, data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'success')

    def test_login(self):
        """
        try login function with correct user info
        """
        url = reverse('backend.personal.views.login')
        data = {
            "email": "abc@132.com",
            "password" : "1111"
        }
        data = json.dumps(data)
        response = self.client.post(url, data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], "success")

    def test_logout(self):
        """
        try logout function with a token from a online user
        """
        url = reverse('backend.personal.views.logout')
        data = {
            'token': 'test'
        }
        data = json.dumps(data)
        response = self.client.post(url, data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data['status'], "success")
    def test_edit(self):
        university = University.objects.get(id = 1)
        url = reverse('backend.personal.views.edit')
        data =  {
            "token": "test",
            "data": {
                "first_name" : "test",
                "last_name"  : "wang",
                "nick_name"  : "haha",
                "password"   : "1111",
                "gender"     : "male",
                "image"      : "http",
                "eas_id"     : "0001",
                "tpa_type"   : "1",
                "tpa_id"     : "0321",
                "university" : 1,
                "email"      : "abc@132.com",
                "phone"      : "112333223"
            }
        }
        data = json.dumps(data)
        response = self.client.post(url, data, content_type="application/json")
        new_data = User.objects.get(id=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(new_data.first_name, "test")
    def test_editPw(self):
        url = reverse('backend.personal.views.editPw')
        data =  {
            "token"        : "test",
            "old_password" : "1111",
            "new_password" : "2222"
        }
        data = json.dumps(data)
        response = self.client.post(url, data, content_type="application/json")
        new_data = User.objects.get(id=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(new_data.password, "2222")


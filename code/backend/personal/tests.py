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
from backend.univinfo.models import University, Grade
from backend.personal.models import User, UserState
class PersonalTests(APITestCase):
    def setUp(self):
        self.client = Client()
        University.objects.create(id = 1, name="UCB", address="C", semester=4)
        Grade.objects.create(id = 1, name="test")
        university = University.objects.get(id = 1)
        grade      = Grade.objects.get(id = 1)
        User.objects.create(first_name = "er",
                            last_name = "wang",
                            nick_name = "haha",
                            password  = "1111",
                            gender    = "male",
                            image     = "http",
                            eas_id    = "0001",
                            tpa_type  = "1",
                            tpa_id    = "0321",
                            university= university,
                            grade     = grade,
                            email     = "abc@132.com",
                            phone     = "112333223"
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
                "grade": 1,
                "email": "abc@13.com",
                "phone": "1233211123"
            }
        response = self.client.post(url, data, format='json')
        print response.data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, data)

    def test_login(self):
        """
        try login function with correct user info
        """
        url = reverse('backend.personal.views.login')
        data = {
            "email": "abc@132.com",
            "password" : "1111"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], "success")

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase;
from rest_framework import status;
from ..serializer import *;
from blogging.models import *;
import json;
from blogging import views
from django.contrib.auth.models import User as Admin


# Test cases for API
class UserSerializerTestCase(APITestCase):
    def test_validate_user(self):
        data = {
            "first_name": "John", 
            "last_name": "Doe",  
            "email": "john@doe.com",
            "user_name": "johndoe123",
            "password": "mypass1234567890"
        }
        
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
    def test_invalid_user(self):
        data = {
            "first_name": "",  # Empty first name
            "last_name": "Doe",
            "email": "johndoe",  # Missing @ in email
            "user_name": "a" * 100,  # Username too long
            "password": ""  # Password is too short
        }

        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())

        # Check individual fields for error messages
        self.assertEqual(serializer.errors['first_name'][0], 'This field may not be blank.')
        self.assertEqual(serializer.errors['email'][0], 'Enter a valid email address.')

        # Check password length validation
        password = data.get('password')
        self.assertIsNotNone(password)
        self.assertTrue(len(password) < 4, 'Password must be at least 4 characters')



    def test_existing_username(self):
        # Create a user with an existing username
        User.objects.create(
            first_name="John", 
            last_name="Doe",  
            email="existing@example.com",
            user_name="johndoe123",
            password="existingpassword"
        )
        
        data = {
            "first_name": "Jane", 
            "last_name": "Doe",  
            "email": "jane@doe.com",
            "user_name": "johndoe123", # Existing username
            "password": "janepassword"
        }
        
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())



class TestAPI(TestCase):
    def test_get_csrf_cookie(self):
        response = self.client.get(reverse("get_csrf_cookie"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("csrftoken", response.cookies)

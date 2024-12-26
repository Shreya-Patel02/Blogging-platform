from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from rest_framework import status

class UserCreationTests(TestCase):
    
    def setUp(self):
        # Create test users
        self.owner = get_user_model().objects.create_user(username='owner', password='ownerpass', role='Owner')
        self.admin = get_user_model().objects.create_user(username='admin', password='adminpass', role='Admin')
        self.member = get_user_model().objects.create_user(username='member', password='memberpass', role='Member')
        
        # URL for user registration
        self.register_url = reverse('register-page')
        
    def test_owner_can_create_admin_and_member(self):
        # Log in as Owner
        self.client.login(username='owner', password='ownerpass')
        
        # Create Admin user
        response = self.client.post(self.register_url, data={'username': 'new_admin', 'role': 'Admin'})
        self.assertEqual(response.status_code, 302)  # Should redirect on success
        self.assertRedirects(response, '/login/')  # After successful creation, redirect to login
        
        # Check if the new Admin user was actually created
        new_admin = get_user_model().objects.get(username='new_admin')
        self.assertEqual(new_admin.role, 'Admin')
        
        # Create Member user
        response = self.client.post(self.register_url, data={'username': 'new_member', 'role': 'Member'})
        self.assertEqual(response.status_code, 302)  # Should redirect on success
        self.assertRedirects(response, '/login/')  # After successful creation, redirect to login
        
        # Check if the new Member user was actually created
        new_member = get_user_model().objects.get(username='new_member')
        self.assertEqual(new_member.role, 'Member')
        
    def test_admin_cannot_create_user(self):
        # Log in as Admin
        self.client.login(username='admin', password='adminpass')
        
        # Try creating a new user (should be forbidden)
        response = self.client.post(self.register_url, data={'username': 'unauthorized_user', 'role': 'Member'})
        self.assertEqual(response.status_code, 403)  # Admin should not be allowed to create users
        
    def test_member_cannot_create_user(self):
        # Log in as Member
        self.client.login(username='member', password='memberpass')
        
        # Try creating a new user (should be forbidden)
        response = self.client.post(self.register_url, data={'username': 'unauthorized_user', 'role': 'Member'})
        self.assertEqual(response.status_code, 403)  # Member should not be allowed to create users

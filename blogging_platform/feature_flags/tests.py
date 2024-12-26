from django.test import TestCase
from django.urls import reverse
from users.models import User
from feature_flags.models import FeatureFlags

class FeatureFlagTests(TestCase):
    def setUp(self):
        # Create an Owner user (who can toggle feature flags)
        self.owner = User.objects.create_user(username='owner', password='password', role='Owner')
        
        # Create a non-owner user (this user should not have permission to toggle feature flags)
        self.non_owner = User.objects.create_user(username='non_owner', password='password', role='Member')
        
        # Create a FeatureFlags object
        self.flags = FeatureFlags.objects.create(
            llm_article_generation=False, 
            llm_tags_generation=False
        )

        # Define the URL for feature flags
        self.feature_flags_url = reverse('feature_flags')

    def test_feature_flags_page_access_for_owner(self):
        # Test that the owner can access the feature flags page
        self.client.login(username='owner', password='password')
        response = self.client.get(self.feature_flags_url)
        self.assertEqual(response.status_code, 200)  # Owner should be able to access
        self.assertContains(response, "LLM Article Generation: off")
        self.assertContains(response, "LLM Tags Generation: off")

    def test_feature_flags_page_access_for_non_owner(self):
        # Test that non-owners cannot access the feature flags page
        self.client.login(username='non_owner', password='password')
        response = self.client.get(self.feature_flags_url)
        self.assertEqual(response.status_code, 403)  # Non-owners should be denied access

    def test_toggle_feature_flags(self):
        # Test that the owner can toggle the feature flags
        self.client.login(username='owner', password='password')
        
        # Toggle llm_article_generation flag
        response = self.client.post(self.feature_flags_url, data={
            'llm_article_generation': 'on',
            'llm_tags_generation': 'off'
        })
        self.assertEqual(response.status_code, 302)  # Ensure the response is successful
        self.assertRedirects(response, '/')
        # Check if the flags were updated correctly
        self.flags.refresh_from_db()
        self.assertTrue(self.flags.llm_article_generation)  # Flag should be set to True
        self.assertFalse(self.flags.llm_tags_generation)    # Flag should remain False

    def test_feature_flags_initial_state(self):
        # Test that the feature flags are created with the initial state correctly
        self.client.login(username='owner', password='password')
        response = self.client.get(self.feature_flags_url)
        self.assertEqual(response.status_code, 200)
        
        # Check that the feature flags are initialized to False
        self.assertContains(response, "LLM Article Generation: off")
        self.assertContains(response, "LLM Tags Generation: off")

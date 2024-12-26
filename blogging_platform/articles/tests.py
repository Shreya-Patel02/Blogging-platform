from django.test import TestCase
from django.urls import reverse
from feature_flags.models import FeatureFlags
from users.models import User
from articles.models import Article

class ArticleTests(TestCase):
    def setUp(self):
        # Create an Owner user (first registered user)
        self.owner = User.objects.create_user(username='owner', password='password', role='Owner')
        # Create an admin user 
        self.admin = User.objects.create_user(username='admin', password='password', role='Admin')
        # Create a Member user
        self.member = User.objects.create_user(username='member', password='password', role='Member')
        
        self.article = Article.objects.create(title="Test Article", content="Sample content", author=self.admin)
        self.flags = FeatureFlags.objects.create(
            llm_article_generation=False, 
            llm_tags_generation=False
        )

    def test_article_creation(self):
        self.client.login(username='admin', password='password')
        response = self.client.post(reverse('article_create'), {'title': 'New Article', 'content': 'New content'})
        self.assertEqual(response.status_code, 302)  # Expect redirect after successful creation

    def test_article_list(self):
        self.client.login(username='member', password='password')
        response = self.client.get(reverse('article_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Article")
    
    def test_article_edit(self):
        self.client.login(username='admin', password='password')
        response = self.client.post(reverse('article_edit', args=[self.article.id]), {'title': 'Updated Article', 'content': 'Updated content'})
        self.assertEqual(response.status_code, 302)  # Expect redirect after successful update

    def test_article_delete(self):
        self.client.login(username='admin', password='password')
        response = self.client.post(reverse('article_delete', args=[self.article.id]))
        self.assertEqual(response.status_code, 302)  # Expect redirect after deletion

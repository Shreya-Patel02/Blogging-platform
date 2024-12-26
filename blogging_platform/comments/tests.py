from django.test import TestCase
from django.urls import reverse
from users.models import User
from articles.models import Article
from comments.models import Comment

class CommentTests(TestCase):
    def setUp(self):
        # Create an Owner user (first registered user)
        self.owner = User.objects.create_user(username='owner', password='password', role='Owner')
        
        # Create an Admin user
        self.admin = User.objects.create_user(username='admin', password='password', role='Admin')
        
        # Create a Member user
        self.member = User.objects.create_user(username='member', password='password', role='Member')

        # Create an article
        self.article = Article.objects.create(title="Test Article", content="Sample content", author=self.owner)

    def test_comment_creation_by_member(self):
        # Test that a Member user can create a comment
        self.client.login(username='member', password='password')
        response = self.client.post(reverse('comment_create', args=[self.article.id]), {'content': 'Great article!'})
        self.assertEqual(response.status_code, 302)  # Expect redirect to article detail page after successful creation

    def test_comment_creation_by_admin(self):
        # Test that an Admin user can create a comment
        self.client.login(username='admin', password='password')
        response = self.client.post(reverse('comment_create', args=[self.article.id]), {'content': 'Awesome post!'})
        self.assertEqual(response.status_code, 302)  # Expect redirect to article detail page after successful creation

    def test_comment_list(self):
        # Test that the list of comments for an article is displayed
        self.client.login(username='member', password='password')
        # Create a comment for the article
        Comment.objects.create(content="Nice article!", article=self.article, user=self.member)
        response = self.client.get(reverse('comment_list', args=[self.article.id]))
        self.assertEqual(response.status_code, 200)  # Ensure the page loads successfully
        self.assertContains(response, "Nice article!")  # Ensure the comment is displayed

    def test_comment_creation_by_owner(self):
        # Test that the Owner user can create a comment
        self.client.login(username='owner', password='password')
        response = self.client.post(reverse('comment_create', args=[self.article.id]), {'content': 'Great article from the owner!'})
        self.assertEqual(response.status_code, 302)  # Expect redirect to article detail page after successful creation

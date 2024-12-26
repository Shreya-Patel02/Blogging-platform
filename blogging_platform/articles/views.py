from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from fastapi import Response
from feature_flags.models import FeatureFlags
from users.permissions import IsOwner, IsAdmin, IsMember
from utils import generate_content, generate_tags
from .models import Article
from .forms import ArticleForm
from django.contrib import messages
from rest_framework.views import APIView

class ArticleCreateView(APIView):
    permission_classes = [IsOwner | IsAdmin]

    def get(self, request):
        form = ArticleForm()
        return render(request, 'articles/article_form.html', {'form': form})

    def post(self, request):
        form = ArticleForm(request.POST)
        flags = FeatureFlags.objects.first()
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user  # Associate the logged-in user as the author

            # Use LLM for content if enabled and not provided
            if flags.llm_article_generation and not article.content :
                article.content = generate_content(f"Write an article about {article.title}")
            if not article.content:  # Check if the content is still empty
                article.content = "Default content generated"

            # Generate tags if the feature is enabled
            if flags.llm_tags_generation and article.content:
                article.tags = generate_tags(article.content)
            if not article.tags:
                article.tags = "Default tag"
            article.save()

            messages.success(request, "Article created successfully!")
            return redirect('article_list')  # Redirect to the article list or another page
        return render(request, 'articles/article_form.html', {'form': form})


class ArticleEditView(APIView):
    permission_classes = [IsOwner | IsAdmin]

    def get(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        # Pre-fill the form with the article data
        form = ArticleForm(instance=article)
        return render(request, 'articles/article_form.html', {'form': form, 'article': article})

    def post(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, "Article updated successfully!")
            return redirect('article_list')  # Redirect to the article list or another page
        return render(request, 'articles/article_form.html', {'form': form, 'article': article})


class ArticleDeleteView(APIView):
    permission_classes = [IsOwner | IsAdmin]

    def delete_article(self, request, article_id):
        """Helper function to delete an article if user has the right permissions."""
        article = get_object_or_404(Article, id=article_id)
        article.delete()
        messages.success(request, "Article deleted successfully!")
        return redirect('article_list')  # Redirect to the article list or another page

    def get(self, request, article_id):
        return self.delete_article(request, article_id)

    def post(self, request, article_id):
        return self.delete_article(request, article_id)

class ArticleListView(APIView):
    permission_classes = [IsMember | IsAdmin | IsOwner]

    def get(self, request):
        articles = Article.objects.all()
        return render(request, 'articles/article_list.html', {'articles': articles})

class ArticleDetailView(APIView):
    permission_classes = [IsMember | IsAdmin | IsOwner]  # Ensure that the user is authenticated
    
    def get(self, request, article_id, format=None):
        # Fetch the article from the database
        article = Article.objects.filter(id=article_id).first()
        
        if not article:
            # If article is not found, render a 404 page or handle the error
            return render(request, '404.html', {"error": "Article not found."})

        # If article is found, render the article_detail template
        return render(request, 'articles/article_detail.html', {'article': article})

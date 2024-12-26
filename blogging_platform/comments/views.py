from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from users.permissions import IsOwner, IsAdmin, IsMember
from .models import Article, Comment
from .forms import CommentForm
from django.contrib import messages
from rest_framework.views import APIView

class CommentCreateView(APIView):
    permission_classes = [IsMember | IsAdmin | IsOwner]

    def get(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        form = CommentForm()  # Initialize an empty form for GET requests
        return render(request, 'comments/comment_form.html', {'form': form, 'article': article})

    def post(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.user = request.user  # Associate the logged-in user with the comment
            comment.save()
            messages.success(request, "Comment added successfully!")
            return redirect('article_detail', article_id=article.id)  # Redirect to article detail view
        return render(request, 'comments/comment_form.html', {'form': form})

class CommentListView(APIView):
    permission_classes = [IsMember | IsAdmin | IsOwner]

    def get(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        comments = Comment.objects.filter(article=article)
        return render(request, 'comments/comment_list.html', {'comments': comments, 'article': article})

# comments/urls.py
from django.urls import path
from .views import (
    CommentCreateView,
    CommentListView
)

urlpatterns = [
    # Comment URLs
    path('<int:article_id>/comment/', CommentCreateView.as_view(), name='comment_create'),  # Create Comment
    path('<int:article_id>/comments/', CommentListView.as_view(), name='comment_list'),  # List Comments
]

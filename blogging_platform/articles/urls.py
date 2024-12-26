# articles/urls.py
from django.urls import path
from .views import (
    ArticleCreateView,
    ArticleDetailView,
    ArticleEditView,
    ArticleDeleteView,
    ArticleListView,
)

urlpatterns = [
    # Article URLs
    path('create/', ArticleCreateView.as_view(), name='article_create'),  # Create Article
    path('edit/<int:article_id>/', ArticleEditView.as_view(), name='article_edit'),  # Edit Article
    path('delete/<int:article_id>/', ArticleDeleteView.as_view(), name='article_delete'),  # Delete Article
    path('', ArticleListView.as_view(), name='article_list'),  # List Articles
    path('<int:article_id>/', ArticleDetailView.as_view(), name='article_detail'),
]

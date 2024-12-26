from django.contrib import admin
from .models import Article
from users.permissions import IsOwner, IsAdmin, IsMember

class ArticleAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Allow only Owners and Admins to create articles
        if request.user.role == 'Owner' or request.user.role == 'Admin':
            return True
        return False

    def has_change_permission(self, request, obj=None):
        # Allow only Owners and Admins to edit articles
        if request.user.role == 'Owner' or request.user.role == 'Admin':
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        # Allow only Owners and Admins to delete articles
        if request.user.role == 'Owner' or request.user.role == 'Admin':
            return True
        return False

admin.site.register(Article, ArticleAdmin)


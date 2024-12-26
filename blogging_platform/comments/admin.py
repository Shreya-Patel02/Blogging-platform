from django.contrib import admin
from .models import Comment
from users.permissions import IsOwner, IsAdmin, IsMember

class CommentAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if request.user.role == 'Owner' or request.user.role == 'Admin'or request.user.role == 'Member':
            return True
        return False

    def has_view_permission(self, request, obj=None):
        if request.user.role == 'Owner' or request.user.role == 'Admin' or request.user.role == 'Member':
            return True
        return False

admin.site.register(Comment, CommentAdmin)
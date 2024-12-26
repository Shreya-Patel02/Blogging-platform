from django.urls import path

from feature_flags.views import toggle_feature_flags



urlpatterns = [
    path('', toggle_feature_flags.as_view(), name='feature_flags'),
]
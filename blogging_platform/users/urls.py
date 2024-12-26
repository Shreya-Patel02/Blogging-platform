from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from users.views import home_view, register_page

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', register_page, name='register-page'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]
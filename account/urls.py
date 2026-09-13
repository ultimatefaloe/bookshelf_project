from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from .forms import LoginForm

app_name='account'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='account/login.html',
        authentication_form=LoginForm,
        redirect_authenticated_user=True,
    ), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('reset-password/', views.reset_password_view, name='reset_password'),
    path('reset-password/done/', views.reset_password_done_view, name='reset_password_done'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
]

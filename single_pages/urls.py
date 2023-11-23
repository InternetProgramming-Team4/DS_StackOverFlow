from django.urls import path
from . import views

app_name = 'single_pages'
urlpatterns = [
    path('MyPage/', views.user, name='MyPage'),
    path('', views.main, name='main'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
]
from django.urls import path
from . import views

urlpatterns=[
    path('MyPage/', views.user,name='MyPage'),
    path('', views.main,name='main'),
    path('login/', views.login,name='login'),
    path('signup/', views.signup,name='signup'),
]
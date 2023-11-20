from django.urls import path
from . import views

urlpatterns=[
    path('MyPage/', views.user),
    path('', views.main),
    path('login/', views.login),
    path('signup/', views.signup),
]
from django.urls import path
from . import views

urlpatterns = [
    path('<str:slug>/', views.major_page),
]
from django.urls import path
from . import views

app_name='post'
urlpatterns = [
    path('', views.nomajorlist),
    path('<str:slug>/', views.major_page, name='Qlist'),
    path('<str:slug>/<int:pk>/', views.PostDetail.as_view()),
]
from django.urls import path
from . import views

app_name='post'
urlpatterns = [
    path('', views.nomajorlist),
    path('create_post/', views.PostCreate.as_view(), name='create_post'),
    path('<str:slug>/', views.major_page, name='Qlist'),
    path('<str:slug>/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('<str:slug>/<int:pk>/upvote_post/', views.UpvotePostView.as_view(), name='upvote_post'),
    path('<str:slug>/<int:pk>/downvote_post/', views.DownvotePostView.as_view(), name='downvote_post'),
]
from django.urls import path
from . import views

app_name='post'
urlpatterns = [
    path('', views.nomajorlist),
    path('<str:slug>/', views.major_page, name='Qlist'),
    path('<str:slug>/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('<str:slug>/<int:pk>/upvote/', views.UpvotePostView.as_view(), name='upvote_post'),
    path('<str:slug>/<int:pk>/downvote/', views.DownvotePostView.as_view(), name='downvote_post'),
]
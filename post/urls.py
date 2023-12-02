from django.urls import path
from . import views

app_name='post'
urlpatterns = [
    path('', views.nomajorlist),
    path('create_post/', views.PostCreate.as_view(), name='create_post'),
    path('delete_post/<int:pk>', views.PostDelete.as_view(), name='delete_post'),
    path('update_post/<int:pk>', views.PostUpdate.as_view(), name='update_post'),
    path('update_comment/<int:pk>', views.CommentUpdate.as_view(), name='update_comment'),
    path('delete_comment/<int:pk>', views.delete_comment, name='delete_comment'),
    path('<str:slug>/', views.major_page, name='Qlist'),
    path('<str:slug>/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('<str:slug>/<int:pk>/upvote_post/', views.UpvotePostView.as_view(), name='upvote_post'),
    path('<str:slug>/<int:pk>/downvote_post/', views.DownvotePostView.as_view(), name='downvote_post'),
    path('<str:slug>/<int:pk>/new_comment/', views.new_comment),
    path('<str:slug>/<int:pk>/upvote_comment/<int:comment_pk>', views.UpvoteCommentView.as_view(), name='upvote_comment'),
    path('<str:slug>/<int:pk>/downvote_comment//<int:comment_pk>', views.DownvoteCommentView.as_view(), name='downvote_comment'),
    path('search/', views.PostSearchView.as_view(), name='post_searched'),
]

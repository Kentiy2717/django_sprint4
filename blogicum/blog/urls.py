from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.IndexListView.as_view(), name='index'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/create/',
         views.PostCreateView.as_view(),
         name='create_post'),
    path('posts/<int:post_id>/edit/',
         views.PostUpdateView.as_view(),
         name='edit_post'),
    path('posts/<int:post_id>/delete/',
         views.PostDeleteView.as_view(),
         name='delete_post'),
    path('posts/<int:post_id>/comment/',
         views.AddCommentCreateView.as_view(),
         name='add_comment'),
    path('posts/<int:post_id>/edit_comment/<int:comment_id>/',
         views.EditCommentUpdateView.as_view(),
         name='edit_comment'),
    path('posts/<int:post_id>/delete_comment/<int:comment_id>/',
         views.DeleteCommentDeleteView.as_view(),
         name='delete_comment'),
    path('category/<slug:category_slug>/', views.CategoryPostListView.as_view(),
         name='category_posts'),
    path('profile/<slug:username>/', views.ProfileListView.as_view(),
         name='profile'),
    path('profile/<slug:username>/edit/',
         views.ProfileUpdateView.as_view(),
         name='edit_profile'),
]
from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('posts/', views.posts, name='posts'),
	path('posts/<int:post_id>/', views.post, name='post'),
	path('new_post/', views.new_post, name='new_post'),
	path('new_comment/<int:post_id>/', views.new_comment, name='new_comment'),
	path('edit_comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
]
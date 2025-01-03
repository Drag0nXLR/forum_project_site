from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .forms import PostForm, CommentForm
from .models import Post, Comment

def index(request):
	"""
	Renders the index page for the forum.

	:return: rendered index page
	"""

	return render(request, 'forums/index.html')

def posts(request):
	"""
	Displays all posts.

	:return: rendered page with a list of all posts
	"""
	posts = Post.objects.all().order_by('-date_added')
	context = {'posts': posts}
	return render(request, 'forums/posts.html', context)

def post(request, post_id):
	"""
	Displays a single post, with all its comments ordered by date added (newest first).

	:param request: the request object
	:param post_id: the id of the post to display
	:return: rendered page with a single post and its comments
	"""
	post = Post.objects.get(id=post_id)
	comments = post.comment_set.order_by('-date_added')
	context = {'post': post, 'comments': comments}
	return render(request, 'forums/post.html', context)

@login_required
def new_post(request):
	"""
	Displays a form for adding a new post, processes the submitted data and redirects
	to the posts page after saving the post.

	:param request: the request object
	:return: rendered page with a post form or redirect to posts page
	"""
	if request.method != 'POST':
		# No data submitted; create a blank form.
		form = PostForm()
	else:
		# POST data submitted; process data.
		form = PostForm(data=request.POST)
		if form.is_valid():
			new_post = form.save(commit=False)
			new_post.author = request.user
			new_post.save()
			return redirect('posts')

	context = {'form': form}
	return render(request, 'forums/new_post.html', context)

@login_required
def new_comment(request, post_id):
	"""
	Displays a form for adding a new comment to a post, processes the
	submitted data and redirects to the post page after saving the
	comment.

	:param request: the request object
	:param post_id: the id of the post the comment will be added to
	:return: rendered page with a comment form or redirect to post page
	"""
	post = Post.objects.get(id=post_id)
	if request.method != 'POST':
		# No data submitted; create a blank form.
		form = CommentForm()
	else:
		# POST data submitted; process data.
		form = CommentForm(data=request.POST)
		if form.is_valid():
			new_comment = form.save(commit=False)
			new_comment.post = post
			new_comment.author = request.user
			new_comment.save()
			return redirect('post', post_id=post_id)

	context = {'post': post, 'form': form}
	return render(request, 'forums/new_comment.html', context)

@login_required
def edit_comment(request, comment_id):
	"""
	Displays a form for editing a comment, processes the submitted data and redirects
	to the post page after saving the comment.

	:param request: the request object
	:param comment_id: the id of the comment to edit
	:return: rendered page with a comment form or redirect to post page
	"""
	comment = Comment.objects.get(id=comment_id)
	post = comment.post

	# Ensure that the comment belongs to the current user.
	if comment.author != request.user:
		raise Http404

	if request.method != 'POST':
		# No data submitted; create a form pre-filled with the comment's content.
		form = CommentForm(instance=comment)
	else:
		# POST data submitted; process data.
		form = CommentForm(instance=comment, data=request.POST)
		if form.is_valid():
			form.save()
			return redirect('post', post_id=post.id)

	context = {'post': post, 'comment': comment, 'form': form}
	return render(request, 'forums/edit_comment.html', context)
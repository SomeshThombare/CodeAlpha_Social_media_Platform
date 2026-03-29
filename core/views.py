"""
core/views.py
All Views:
  - register_view       → GET/POST /register/
  - login_view          → GET/POST /login/
  - logout_view         → POST     /logout/
  - feed_view           → GET/POST /feed/       (home feed + create post)
  - profile_view        → GET      /profile/<username>/
  - edit_profile_view   → GET/POST /profile/edit/
  - post_detail_view    → GET/POST /post/<id>/   (post + comments)
  - delete_post_view    → POST     /post/<id>/delete/
  - like_post_view      → POST     /post/<id>/like/   (AJAX)
  - follow_view         → POST     /follow/<username>/  (AJAX)
  - search_view         → GET      /search/
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q

from .models import Post, Comment, Like, Follow, Profile
from .forms import RegisterForm, LoginForm, PostForm, CommentForm, ProfileForm


# ─── Utility: Auto-create Profile if missing ─────────────────────────────────
def get_or_create_profile(user):
    profile, _ = Profile.objects.get_or_create(user=user)
    return profile


# ─── 1. Register ─────────────────────────────────────────────────────────────
def register_view(request):
    """Handle new user registration."""
    if request.user.is_authenticated:
        return redirect('feed')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)   # Create profile automatically
            messages.success(request, f'Account created! Welcome, {user.username}!')
            login(request, user)
            return redirect('feed')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = RegisterForm()

    # Template path: core/templates/core/register.html
    return render(request, 'core/register.html', {'form': form})


# ─── 2. Login ────────────────────────────────────────────────────────────────
def login_view(request):
    """Handle user login."""
    if request.user.is_authenticated:
        return redirect('feed')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                get_or_create_profile(user)   # Ensure profile exists
                next_url = request.GET.get('next', 'feed')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    # Template path: core/templates/core/login.html
    return render(request, 'core/login.html', {'form': form})


# ─── 3. Logout ───────────────────────────────────────────────────────────────
@login_required
def logout_view(request):
    """Log out and redirect to login."""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')


# ─── 4. Feed ─────────────────────────────────────────────────────────────────
@login_required
def feed_view(request):
    """
    Home feed: shows posts from followed users + own posts.
    Also handles new post creation.
    """
    get_or_create_profile(request.user)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created!')
            return redirect('feed')
    else:
        form = PostForm()

    # Get IDs of users current user follows
    following_ids = Follow.objects.filter(
        follower=request.user
    ).values_list('following_id', flat=True)

    # Posts from followed users + own posts
    posts = Post.objects.filter(
        Q(author__in=following_ids) | Q(author=request.user)
    ).select_related('author', 'author__profile').prefetch_related('likes', 'comments')

    # Add liked status for each post
    liked_post_ids = Like.objects.filter(
        user=request.user
    ).values_list('post_id', flat=True)

    context = {
        'form': form,
        'posts': posts,
        'liked_post_ids': list(liked_post_ids),
    }

    # Template path: core/templates/core/feed.html
    return render(request, 'core/feed.html', context)


# ─── 5. Profile ──────────────────────────────────────────────────────────────
@login_required
def profile_view(request, username):
    """Show a user's profile with their posts."""
    profile_user = get_object_or_404(User, username=username)
    profile = get_or_create_profile(profile_user)

    posts = Post.objects.filter(author=profile_user).select_related('author')

    is_following = Follow.objects.filter(
        follower=request.user,
        following=profile_user
    ).exists()

    followers_count  = Follow.objects.filter(following=profile_user).count()
    following_count  = Follow.objects.filter(follower=profile_user).count()

    liked_post_ids = Like.objects.filter(
        user=request.user
    ).values_list('post_id', flat=True)

    context = {
        'profile_user':    profile_user,
        'profile':         profile,
        'posts':           posts,
        'is_following':    is_following,
        'followers_count': followers_count,
        'following_count': following_count,
        'posts_count':     posts.count(),
        'liked_post_ids':  list(liked_post_ids),
        'is_own_profile':  (request.user == profile_user),
    }

    # Template path: core/templates/core/profile.html
    return render(request, 'core/profile.html', context)


# ─── 6. Edit Profile ─────────────────────────────────────────────────────────
@login_required
def edit_profile_view(request):
    """Edit current user's bio and avatar."""
    profile = get_or_create_profile(request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated!')
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'core/edit_profile.html', {'form': form})


# ─── 7. Post Detail + Comments ───────────────────────────────────────────────
@login_required
def post_detail_view(request, post_id):
    """Show single post with all comments. Handle new comment submission."""
    post     = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post).select_related('author', 'author__profile')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment        = form.save(commit=False)
            comment.post   = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added!')
            return redirect('post_detail', post_id=post_id)
    else:
        form = CommentForm()

    is_liked = Like.objects.filter(post=post, user=request.user).exists()

    context = {
        'post':     post,
        'comments': comments,
        'form':     form,
        'is_liked': is_liked,
    }

    # Template path: core/templates/core/post_detail.html
    return render(request, 'core/post_detail.html', context)


# ─── 8. Delete Post ──────────────────────────────────────────────────────────
@login_required
def delete_post_view(request, post_id):
    """Delete a post (only by its author)."""
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted.')
    return redirect('feed')


# ─── 9. Like / Unlike (AJAX) ─────────────────────────────────────────────────
@login_required
def like_post_view(request, post_id):
    """Toggle like on a post. Returns JSON for AJAX calls."""
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(post=post, user=request.user)

        if not created:
            like.delete()   # Unlike
            liked = False
        else:
            liked = True

        return JsonResponse({
            'liked':       liked,
            'likes_count': Like.objects.filter(post=post).count()
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)


# ─── 10. Follow / Unfollow (AJAX) ────────────────────────────────────────────
@login_required
def follow_view(request, username):
    """Toggle follow on a user. Returns JSON."""
    if request.method == 'POST':
        target_user = get_object_or_404(User, username=username)

        if target_user == request.user:
            return JsonResponse({'error': "You can't follow yourself."}, status=400)

        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            following=target_user
        )

        if not created:
            follow.delete()   # Unfollow
            following = False
        else:
            following = True

        return JsonResponse({
            'following':       following,
            'followers_count': Follow.objects.filter(following=target_user).count()
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)


# ─── 11. Search Users ────────────────────────────────────────────────────────
@login_required
def search_view(request):
    """Search for users by username or name."""
    query   = request.GET.get('q', '').strip()
    results = []

    if query:
        results = User.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        ).exclude(id=request.user.id).select_related('profile')

    # Which of these are followed by current user?
    following_ids = Follow.objects.filter(
        follower=request.user
    ).values_list('following_id', flat=True)

    context = {
        'query':         query,
        'results':       results,
        'following_ids': list(following_ids),
    }

    # Template path: core/templates/core/search.html
    return render(request, 'core/search.html', context)

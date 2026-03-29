"""
core/urls.py  ←  App-level URL patterns
All URLs for the social media app.
"""

from django.urls import path
from . import views

urlpatterns = [
    # ─── Auth ────────────────────────────────────────────────────────────────
    path('',           views.login_view,    name='home'),      # Root → login
    path('register/',  views.register_view, name='register'),
    path('login/',     views.login_view,    name='login'),
    path('logout/',    views.logout_view,   name='logout'),

    # ─── Feed ────────────────────────────────────────────────────────────────
    path('feed/',      views.feed_view,     name='feed'),

    # ─── Profile ─────────────────────────────────────────────────────────────
    path('profile/<str:username>/',  views.profile_view,      name='profile'),
    path('profile/edit/',            views.edit_profile_view, name='edit_profile'),

    # ─── Posts ───────────────────────────────────────────────────────────────
    path('post/<int:post_id>/',         views.post_detail_view, name='post_detail'),
    path('post/<int:post_id>/delete/',  views.delete_post_view, name='delete_post'),

    # ─── Like & Follow (AJAX endpoints) ──────────────────────────────────────
    path('post/<int:post_id>/like/',    views.like_post_view,  name='like_post'),
    path('follow/<str:username>/',      views.follow_view,     name='follow'),

    # ─── Search ──────────────────────────────────────────────────────────────
    path('search/',    views.search_view,  name='search'),
]

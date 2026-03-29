"""
core/models.py
Database Models:
  - Profile  (extends built-in User)
  - Post     (user posts with image support)
  - Comment  (comments on posts)
  - Like     (like a post)
  - Follow   (follow/unfollow users)
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# ─── 1. Profile ───────────────────────────────────────────────────────────────
class Profile(models.Model):
    """
    Extends Django's built-in User model.
    One Profile per User (OneToOne).
    """
    user        = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio         = models.TextField(max_length=300, blank=True, default='')
    avatar      = models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at  = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username} Profile'

    def get_followers_count(self):
        return Follow.objects.filter(following=self.user).count()

    def get_following_count(self):
        return Follow.objects.filter(follower=self.user).count()

    def get_posts_count(self):
        return Post.objects.filter(author=self.user).count()


# ─── 2. Post ──────────────────────────────────────────────────────────────────
class Post(models.Model):
    """
    A post created by a user.
    """
    author      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content     = models.TextField(max_length=500)
    image       = models.ImageField(upload_to='posts/', blank=True, null=True)
    created_at  = models.DateTimeField(default=timezone.now)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']   # Newest posts first

    def __str__(self):
        return f'Post by {self.author.username} at {self.created_at.strftime("%Y-%m-%d %H:%M")}'

    def get_likes_count(self):
        return Like.objects.filter(post=self).count()

    def get_comments_count(self):
        return Comment.objects.filter(post=self).count()

    def is_liked_by(self, user):
        """Check if a given user has liked this post."""
        return Like.objects.filter(post=self, user=user).exists()


# ─── 3. Comment ───────────────────────────────────────────────────────────────
class Comment(models.Model):
    """
    A comment on a Post.
    """
    post        = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content     = models.TextField(max_length=300)
    created_at  = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['created_at']    # Oldest comments first (top to bottom)

    def __str__(self):
        return f'Comment by {self.author.username} on Post #{self.post.id}'


# ─── 4. Like ──────────────────────────────────────────────────────────────────
class Like(models.Model):
    """
    A user likes a post. One like per user per post (unique_together).
    """
    post        = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    created_at  = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('post', 'user')   # Prevent duplicate likes

    def __str__(self):
        return f'{self.user.username} liked Post #{self.post.id}'


# ─── 5. Follow ────────────────────────────────────────────────────────────────
class Follow(models.Model):
    """
    User A (follower) follows User B (following).
    unique_together prevents duplicate follows.
    """
    follower    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following   = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at  = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('follower', 'following')  # Can't follow same person twice

    def __str__(self):
        return f'{self.follower.username} follows {self.following.username}'

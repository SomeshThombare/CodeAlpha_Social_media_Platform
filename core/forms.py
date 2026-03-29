"""
core/forms.py
All Django Forms:
  - RegisterForm   - New user registration
  - LoginForm      - User login
  - PostForm       - Create/edit a post
  - CommentForm    - Add a comment
  - ProfileForm    - Edit profile (bio, avatar)
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment, Profile


# ─── 1. Register Form ─────────────────────────────────────────────────────────
class RegisterForm(UserCreationForm):
    email       = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'placeholder': 'Enter your email',
        'class': 'form-input'
    }))
    first_name  = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'placeholder': 'First name',
        'class': 'form-input'
    }))
    last_name   = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'placeholder': 'Last name',
        'class': 'form-input'
    }))

    class Meta:
        model   = User
        fields  = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Choose a username', 'class': 'form-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'placeholder': 'Create password', 'class': 'form-input'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm password', 'class': 'form-input'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email


# ─── 2. Login Form ────────────────────────────────────────────────────────────
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Username',
        'class': 'form-input'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'form-input'
    }))


# ─── 3. Post Form ─────────────────────────────────────────────────────────────
class PostForm(forms.ModelForm):
    class Meta:
        model   = Post
        fields  = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': "What's on your mind?",
                'class': 'post-textarea',
                'rows': 3
            }),
            'image': forms.FileInput(attrs={'class': 'file-input'}),
        }


# ─── 4. Comment Form ──────────────────────────────────────────────────────────
class CommentForm(forms.ModelForm):
    class Meta:
        model   = Comment
        fields  = ['content']
        widgets = {
            'content': forms.TextInput(attrs={
                'placeholder': 'Write a comment...',
                'class': 'comment-input'
            }),
        }


# ─── 5. Profile Edit Form ─────────────────────────────────────────────────────
class ProfileForm(forms.ModelForm):
    class Meta:
        model   = Profile
        fields  = ['bio', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={
                'placeholder': 'Write something about yourself...',
                'class': 'form-input',
                'rows': 3
            }),
            'avatar': forms.FileInput(attrs={'class': 'file-input'}),
        }

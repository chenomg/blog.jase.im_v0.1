#!/usr/bin/env python
# encoding: utf-8

from django import forms
from django.contrib.auth.models import User
from mdeditor.fields import MDTextFormField
from .models import Comment, UserProfile, Post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'name', 'email']

    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '发表你的想法///',
            }, ), )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'type': 'email',
            }, ), )

    name = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'type': 'text',
                'rows': 1,
            }, ), )


class UserUpdateForm(forms.Form):
    """
    用于更新用户信息时检查输入信息是否正确
    """
    email = forms.EmailField(required=True)
    website = forms.URLField(initial="http://", required=False)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['website', 'picture']


class MDEditorModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'excerpt',
            'category',
            'tags',
            'content',
        ]

#!/usr/bin/env python
# encoding: utf-8

from django import forms
from django.contrib.auth.models import User
from .models import Comment, UserProfile


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


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['website', 'picture']

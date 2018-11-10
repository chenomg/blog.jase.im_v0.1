#!/usr/bin/env python
# encoding: utf-8

from django import forms
from .models import Comment


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

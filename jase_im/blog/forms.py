#!/usr/bin/env python
# encoding: utf-8

from django import forms
from django.contrib.auth.models import User
# from django.utils.datastructures import SortedDict
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


class MDEditorModelForm(forms.ModelForm, forms.Form):
    add_tags = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': '多个标签以","分开',
                'class': 'form-control col-sm-12 col-md-6',
            }))

    class Meta:
        model = Post
        fields = [
            'title',
            'category',
            'tags',
            'add_tags',
            'excerpt',
            'content',
        ]
        widgets = {
            'title':
            forms.TextInput(
                attrs={
                    'id': 'id_title',
                    'class': 'form-control col-sm-12 col-md-6',
                    'placeholder': 'Title Input',
                }),
            'excerpt':
            forms.TextInput(
                attrs={
                    'id': 'id_excerpt',
                    'class': 'form-control col-sm-12 col-md-6',
                    'rows': '3',
                    'placeholder': 'Excerpt Input',
                }),
            'category':
            forms.Select(attrs={
                'id': 'id_category',
                'class': 'form-control col-sm-12 col-md-6',
            }),
            'tags':
            forms.SelectMultiple(attrs={
                'id': 'id_tags',
                'class': 'form-control col-sm-12 col-md-6',
            }),
        }
        labels = {
            'excerpt': 'Excerpt (Optional)',
            'tags': 'Tags (Optional)',
        }

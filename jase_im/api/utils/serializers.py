#!/usr/bin/env python
# encoding: utf-8

from rest_framework import serializers
from blog.models import Post


class PostGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'author', 'publish_content', 'category',
                  'created_time', 'modified_time')


class PostAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'author', 'content', 'excerpt', 'category', 'tags',
                  'is_publish')

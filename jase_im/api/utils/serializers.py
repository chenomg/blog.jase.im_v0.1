#!/usr/bin/env python
# encoding: utf-8

from rest_framework import serializers
from blog.models import Post
from api.models import ImageHostingModel
from api.utils.reverse import get_image_url


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


class ImageGetSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    email = serializers.CharField(source='user.email')

    def get_image_url(self, obj):
        return get_image_url(obj)

    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = ImageHostingModel
        fields = ('title', 'slug', 'username', 'email', 'created_time', 'image_url')
        depth = 0

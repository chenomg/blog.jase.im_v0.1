#!/usr/bin/env python
# encoding: utf-8


from rest_framework.reverse import reverse

def get_image_url(obj):
    return reverse(
            'image-detail', kwargs={
                'version': 'v1',
                'slug': obj.slug
            })

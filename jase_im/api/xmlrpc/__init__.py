#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""XML-RPC methods"""

XMLRPC_METHODS = (
    ('api.xmlrpc.metaweblog.get_users_blogs', 'blogger.getUsersBlogs'),
    ('api.xmlrpc.metaweblog.get_user_info',
     'blogger.getUserInfo'), ('api.xmlrpc.metaweblog.delete_post',
                              'blogger.deletePost'),
    ('api.xmlrpc.metaweblog.get_authors',
     'wp.getAuthors'), ('api.xmlrpc.metaweblog.get_tags',
                        'wp.getTags'), ('api.xmlrpc.metaweblog.get_categories',
                                        'metaWeblog.getCategories'),
    ('api.xmlrpc.metaweblog.new_category',
     'wp.newCategory'), ('api.xmlrpc.metaweblog.get_recent_posts',
                         'metaWeblog.getRecentPosts'),
    ('api.xmlrpc.metaweblog.get_post',
     'metaWeblog.getPost'), ('api.xmlrpc.metaweblog.new_post',
                             'metaWeblog.newPost'),
    ('api.xmlrpc.metaweblog.edit_post',
     'metaWeblog.editPost'), ('api.xmlrpc.metaweblog.new_media_object',
                              'metaWeblog.newMediaObject')
)

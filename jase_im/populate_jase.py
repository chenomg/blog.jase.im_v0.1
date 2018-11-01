#!/usr/bin/env python3
# encoding: utf-8

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jase_im.settings')

import django
django.setup()
from blog.models import Category, Post, Tag


def populate():
    python_posts = [
        {
            'title':
            '中文标题测试Learning Python: From Zero to Hero',
            'content':
            """
中文测试First of all, what is Python? According to its creator, Guido van Rossum, Python is a:

“high-level programming language, and its core design philosophy is all about code readability and a syntax which allows programmers to express concepts in a few lines of code.”
            """,
            'views':
            12,
            'tags': ['program', 'computer'],
        },
        {
            'title':
            'Learning Python: From Zero to Hero',
            'content':
            """
First of all, what is Python? According to its creator, Guido van Rossum, Python is a:

“high-level programming language, and its core design philosophy is all about code readability and a syntax which allows programmers to express concepts in a few lines of code.”
            """,
            'views':
            12,
            'tags': ['program', 'computer'],
        },
        {
            'title':
            'An A-Z of useful Python tricks',
            'content':
            """
Python is one of the world’s most popular, in-demand programming languages. This is for many reasons:

it’s easy to learn
it’s super versatile
it has a huge range of modules and libraries
            """,
            'views':
            22,
            'tags': ['program2', 'computer2'],
        },
        {
            'title': 'Learn Python in 10 Minutes',
            'content': 'Hello World!',
            'views': 3,
            'tags': ['program3', 'computer3'],
        },
    ]
    django_posts = [
        {
            'title':
            'How to scrape websites with Python and BeautifulSoup',
            'content':
            """
There is more information on the Internet than any human can absorb in a lifetime. What you need is not access to that information, but a scalable way to collect, organize, and analyze it.

You need web scraping.
            """,
            'views':
            34,
            'tags': ['HTTP', 'Url'],
        },
        {
            'title':
            'Creating websites using React and Django REST Framework',
            'content':
            """
Lately at work our go to architecture for creating websites is to use a React frontend with a Django REST Framework (DRF) backend. The two are connected by API calls using axios in the frontend. Some Redux is used as well for storing global app state. This is our preferred method as it allows the frontend and backend to be completely decoupled. And as long as we define a list of endpoints and returned data to work with, the frontend and backend can be developed in parallel. This also allows us the option to easily create mobile apps for any of the projects in the future as they can just consume the backend API. On a side note, we’re currently looking at using React Native for future mobile app projects.
            """,
            'views':
            5,
            'tags': ['HTTP'],
        },
        {
            'title':
            'Continuous Integration. CircleCI vs Travis CI vs Jenkins',
            'content':
            """
CI definition and its main goal
Continuous Integration (CI) is a software development practice that is based on a frequent integration of the code into a shared repository. Each check-in is then verified by an automated build.
            """,
            'views':
            31,
            'tags': [],
        },
    ]
    other_posts = [
        {
            'title':
            'Build Simple Restful Api With Python and Flask Part 1',
            'content':
            """
I’m going to divide this series into 3 or 4 articles. At the end of the series you would understand how easy to build restful API with flask. In this article we’ll setting our environment and create endpoint that will show “Hello World”.
            """,
            'views':
            5,
            'tags': ['Flask'],
        },
        {
            'title':
            'REST is the new SOAP',
            'content':
            """
Introduction
Some years ago, I developed a new information system in a big telecom company. We had to communicate with an increasing number of web services, exposed by older systems or by business partners.

            """,
            'views':
            21,
            'tags': ['REST'],
        },
    ]
    cats = {
        'Python': {
            "posts": python_posts,
        },
        'Django': {
            "posts": django_posts,
        },
        'Other Frameworks': {
            "posts": other_posts,
        }
    }
    for cat, cat_data in cats.items():
        c = add_cat(cat)
        for p in cat_data['posts']:
            add_post(c, p['title'], p['content'], p['views'], p['tags'])

    for c in Category.objects.all():
        for p in Post.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(p)))


def add_post(cat, title, content, views=0, tags=None):
    p = Post.objects.get_or_create(category=cat, title=title)[0]
    p.content = content
    p.views = views
    if tags:
        for t in tags:
            tt = Tag.objects.get_or_create(name=t)
            p.tags.add(tt[0])
    p.save()
    return p


def add_cat(name):
    c = Category.objects.get_or_create(name=name)[0]
    c.save()
    return c


def add_tag(name):
    t = Tag.objects.get_or_create(name=name)[0]
    t.save()
    return t


if __name__ == "__main__":
    print("Starting blog.jase.im population script...")
    populate()

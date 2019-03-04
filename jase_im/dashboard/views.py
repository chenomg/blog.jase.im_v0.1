from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'dashboard/index.html')


def add_new_post(request):
    return render(request, 'dashboard/add-new-post.html')

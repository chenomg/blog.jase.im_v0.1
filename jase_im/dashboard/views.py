from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from blog.forms import CommentForm, UserProfileForm, UserUpdateForm, MDEditorModelForm

# Create your views here.


@login_required
def index(request):
    return render(request, 'dashboard/index.html')


@login_required
def add_new_post(request):
    post_form = MDEditorModelForm()
    context = {'post_form': post_form}
    return render(request, 'dashboard/add-new-post.html', context=context)


@login_required
def components_blog_posts(request):
    return render(request, 'dashboard/components-blog-posts.html')

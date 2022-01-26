from django.shortcuts import get_object_or_404, render

import markdown
from .models import Category, Post,Tag
import pygments
import re

from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
# Create your views here.


def index(request):
    post_list = Post.objects.all()

    context = {
        'title': 'Homepage',
        'index_title': 'Post Index',
        'post_list': post_list,
    }

    return render(request, 'blog/index.html', context)


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        TocExtension(slugify=slugify),
    ])

    post.text= md.convert(post.text)

    #use for validate the menu item
    rexp=re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc,re.S)
    post.toc = rexp.group(1) if rexp is not None else ''
    context = {
        'title':'< Back',
        'post': post,
    }
    return render(request, 'blog/detail.html', context=context)

def archive(request, year, month):
    post_list= Post.objects.filter(
        time_created__year=year,
        time_created__month=month,
    )

    title= 'Archive in {}/{}'.format(month,year)
    context={
        'title':title,
        'post_list':post_list,
    }

    return render(request,'blog/index.html',context=context)

def category(request,pk):
    category= get_object_or_404(Category,pk=pk)
    post_list= Post.objects.filter(category=category)

    context={
        'title': category.name,
        'post_list':post_list,
    }
    return render(request,'blog/index.html',context=context)

def tag(request,pk):
    tag=get_object_or_404(Tag,pk=pk)
    post_list=Post.objects.filter(tags=tag)

    context={
        'title': tag.name,
        'post_list':post_list,
    }

    return render(request,'blog/index.html',context=context)
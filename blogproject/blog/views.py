from multiprocessing import context
from django.shortcuts import get_object_or_404, render

import markdown
from .models import Category, Post, Tag
import re

from django.utils.text import slugify
from markdown.extensions.toc import TocExtension

from django.views.generic import ListView, DetailView
# Create your views here.


class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'


# def index(request):
#     post_list = Post.objects.all()

#     context = {
#         'title': 'Homepage',
#         'index_title': 'Post Index',
#         'post_list': post_list,
#     }

#     return render(request, 'blog/index.html', context)


# def detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     #views +1
#     post.increase_views()

#     md = markdown.Markdown(extensions=[
#         'markdown.extensions.extra',
#         'markdown.extensions.codehilite',
#         TocExtension(slugify=slugify),
#     ])

#     post.text = md.convert(post.text)

#     # use for validate the menu item
#     rexp = re.search(
#         r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
#     post.toc = rexp.group(1) if rexp is not None else ''
#     context = {
#         'title': '< Back',
#         'post': post,
#     }
#     return render(request, 'blog/detail.html', context=context)


##try to pass extra context (title)
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        post = super().get_object(queryset=None)

        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
        ])

        post.text = md.convert(post.text)

        rexp = re.search(
            r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
        post.toc = rexp.group(1) if rexp is not None else ''

        return post


class ArchiveView(IndexView):
    def get_queryset(self):
        return super().get_queryset().filter(
            time_created__year=self.kwargs.get('year'),
            time_created__month=self.kwargs.get('month'),
        )


# def archive(request, year, month):
#     post_list= Post.objects.filter(
#         time_created__year=year,
#         time_created__month=month,
#     )

#     title= 'Archive in {}/{}'.format(month,year)
#     context={
#         'title':title,
#         'post_list':post_list,
#     }

#     return render(request,'blog/index.html',context=context)

class CategoryView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)

# def category(request,pk):
#     category= get_object_or_404(Category,pk=pk)
#     post_list= Post.objects.filter(category=category)

#     context={
#         'title': category.name,
#         'post_list':post_list,
#     }
#     return render(request,'blog/index.html',context=context)

# def tag(request,pk):
#     tag=get_object_or_404(Tag,pk=pk)
#     post_list=Post.objects.filter(tags=tag)

#     context={
#         'title': tag.name,
#         'post_list':post_list,
#     }

#     return render(request,'blog/index.html',context=context)


class TagView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super().get_queryset().filter(tags=tag)

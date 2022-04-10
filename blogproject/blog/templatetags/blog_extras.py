from atexit import register
from django import template
from ..models import Post,Category,Tag

register=template.Library()

@register.inclusion_tag('blog/inclusions/_recent_posts.html',takes_context=True)
def show_recent_posts(context,num=5):
    return {
        'recent_post_list':Post.objects.order_by('-time_created')[:num],
    }

@register.inclusion_tag('blog/inclusions/_archives.html',takes_context=True)
def show_archives(context):
    return{
        'date_list':Post.objects.dates('time_created','month',order='DESC'),
    }

@register.inclusion_tag('blog/inclusions/_categories.html',takes_context=True)
def show_categories(context):
    return{
        'category_list': Category.objects.all(),
    }

@register.inclusion_tag('blog/inclusions/_tags.html',takes_context=True)
def show_tags(context):
    return{
        'tag_list':Tag.objects.all(),
    }
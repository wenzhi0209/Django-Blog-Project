from dataclasses import field
from django.contrib import admin
from .models import Comment
# Register your models here.
class CommentAdmin(admin.ModelAdmin):
    list_display=['name','email','url','post','time_created']
    fields=['name','email','url','text','post']

admin.site.register(Comment, CommentAdmin)
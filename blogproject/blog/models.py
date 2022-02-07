
from distutils import extension
from turtle import update
from django import views
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import markdown
from django.utils.html import strip_tags

# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name='Category'
        #verbose_name_plural=verbose_name
    

class Tag(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='Tag'
        #verbose_name_plural=verbose_name

class Post(models.Model):
    title=models.CharField('Post Title',max_length=100)
    text=models.TextField("Post's Text")

    time_created=models.DateTimeField('Time Created',default=timezone.now)
    time_modified=models.DateTimeField('Time Edited')

    post_abstract=models.CharField('Abstract',blank=True,max_length=200)

    category=models.ForeignKey(Category,on_delete=models.CASCADE,verbose_name='Post Category')
    tags=models.ManyToManyField(Tag,blank=True,verbose_name='Post Relevant Tag')

    author=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='Author')

    like_count=models.IntegerField('Likes Count',default=0)

    #calculate views
    views=models.PositiveIntegerField(default=0,editable=False)

    def save(self,*args,**kwargs):
        self.time_modified=timezone.now()

        md = markdown.Markdown(extensions=['markdown.extensions.extra','markdown.extensions.codehilite'])

        self.post_abstract=strip_tags(md.convert(self.text))[:50]
        super().save(*args,**kwargs)

    # increse view function
    def increase_views(self):
        self.views +=1 
        self.save(update_fields=['views'])

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={"pk": self.pk})
    


    class Meta:
        verbose_name='Post'
        #verbose_name_plural=verbose_name
        ordering=['-time_created']


    
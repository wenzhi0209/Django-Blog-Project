from django.db import models
from django.utils import timezone
# Create your models here.


class Comment(models.Model):
    name = models.CharField('Name', max_length=50)
    email = models.EmailField('Email')
    url = models.URLField('Personal Url', blank=True)
    text = models.TextField('Content')
    time_created = models.DateTimeField('Time Created', default=timezone.now)
    post = models.ForeignKey(
        'blog.Post', verbose_name='Related Post', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Comment'
        ordering=['-time_created']

    def __str__(self):
        return '{}: {}'.format(self.name, self.text[:20])

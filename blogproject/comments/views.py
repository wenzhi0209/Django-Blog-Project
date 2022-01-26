from django.shortcuts import render,redirect,get_object_or_404
from django.template import context
from blog.models import Post
from django.views.decorators.http import require_POST
from django.contrib import messages

from .forms import CommentForm
# Create your views here.

@require_POST
def comment(request,post_pk):
    
    post= get_object_or_404(Post,pk=post_pk)
    form=CommentForm(request.POST)
    
    if form.is_valid():
        #create the object but not yet save to database
        comment= form.save(commit=False)

        comment.post=post

        comment.save()

        messages.add_message(request,messages.SUCCESS,'Your Comment Post Succesfully', extra_tags='success')

        #can provide url or pass object(it will direct call get_absolutre_url)
        return redirect(post)

    context={
        'post':post,
        'form':form,
    }

    messages.add_message(request,messages.ERROR,'Comment Post Fail, Please modify and resubmit the form.',extra_tags='danger')
    return render(request,'comments/preview.html',context=context)


from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from models import BlogPost
# Create your views here.
def view_post(request, post_id):
    template = loader.get_template('blog/post.html')
    post = BlogPost.objects.get(pk=post_id)
    context = {
        'post_title': post.title,
        'post_deck': post.deck,
        'post_header': post.img_name,
        'post_body': post.post_body
    }
    return HttpResponse(template.render(context, request))

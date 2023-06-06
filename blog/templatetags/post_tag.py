from multiprocessing import active_children, context
from django import template
from blog.models import *


register = template.Library()
@register.inclusion_tag('pages/blog/latest_post.html')
def latest_post():
    context = {
        'l_posts': Post.objects.all()[0:5]
    }
    return context

@register.inclusion_tag('pages/blog/latest_comment.html')
def latest_comment():
    context = {
        'l_comments': Comment.objects.filter(active=True)[:5]
    }
    return context
from hashlib import new
from multiprocessing import context
from turtle import title
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# Create your views here.

def home(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_page) 
    context = {
        'title': 'الصفحة الرئسية',
        'posts': posts,
        'page': page,
    }
    return render(request, 'pages/blog/index.html', context)

def about(request):
    context = {
        'title': 'من انا',
    }
    return render(request, 'pages/blog/about.html', context)

def post_detail(request, id):
    # post_id = get_object_or_404(Post, id=id)
    post_id = Post.objects.get(id=id)
    comments = post_id.comments.filter(active=True)
    # Post Comments  Save
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post_id
            new_comment.save()
            new_comment = CommentForm()
    else:
        comment_form = CommentForm()
    

    context = {
        'title' : post_id,
        'post': post_id,
        'comments': comments,
        'comment_form': comment_form,
    }
    
    return render(request, 'pages/blog/detail.html', context)

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    # fields = ['title', 'content']
    template_name = 'pages/blog/new_post.html'
    form_class = PostCreateForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'pages/blog/post_update.html'
    form_class = PostCreateForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False

class PostDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'pages/blog/post_confirm_delete.html'

    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False

from multiprocessing import context
from django.shortcuts import redirect, render
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate , login, logout
from blog.models import *
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = registerForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            # username = form.cleaned_data['username']
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()
            messages.success(request, f'تهانينا {new_user} لقد تمت العملية بنجاح')
            return redirect('login')
    else:
        form = registerForm(request.POST)

    context = {
        'title' : 'التسجيل', 
        'form' :  registerForm()
    }
    return render(request, 'pages/user/register.html', context)

# def login_user(request):
#     if request.method == 'POST':
#         form = LoginForms()
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('home')
#         else:
#             messages.warning(request, 'تأكد من كلمة المرور او اسم المستخدم')
#     else: 
#         form = LoginForms()
#     context = {
#         'title': 'تسجيل الدخول',
#         'form': form,
#     }
#     return render(request, 'pages/user/login.html', context)

#الطريقة التانية 
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.warning(request, 'تأكد من كلمة المرور او اسم المستخدم')
    context = {
        'title': 'تسجيل الدخول',
    }
    return render(request, 'pages/user/login.html', context)


def logout_user(request):
    logout(request)
    context = {
        'title': 'تسجيل الخروج',
    }
    return render(request, 'pages/user/logout.html', context)

@login_required(login_url='login')
def profile(request):
    posts = Post.objects.filter(author=request.user)
    post_list = Post.objects.filter(author=request.user)
    paginator = Paginator(post_list, 5)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_page) 
    context = {
        'title': 'الملف الشخصي',
        'posts': posts,
        'page': page,
        'post_list': post_list,
    }
    return render(request, 'pages/user/profile.html', context)

def profile_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_vaild() and  profile_form.is_vaild():
            user_form.save()
            profile_form.save()
            messages.success(request, 'تم تحديث الملف الشخصي ')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'title': 'تعديل الملف الشخصي',
        'user_form': user_form, 
        'profile_form': profile_form, 
    }
    return render(request, 'pages/user/profile_update.html', context)
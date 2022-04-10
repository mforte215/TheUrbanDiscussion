from audioop import reverse
from .forms import UserCreateForm
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from .models import Article, Thread, Comment
from django.contrib.auth import authenticate, login
from django.db.models import Max

def IndexView(request):
    article_list = get_list_or_404(Article)
    return render(request, 'app/index.html', {'articles': article_list})

def threadListView(request):
    thread_list = get_list_or_404(Thread)
    sorted_thread_list = sorted(thread_list, key=lambda t: t.latest_comment_date, reverse=True)
    return render(request, 'app/thread-list.html', {'threads': sorted_thread_list})

def LoginView(request):
    if request.method == 'GET':
        context = {}
        if request.user.is_authenticated:
            return render(request, 'app/index.html', context)
        else:
            return render(request, 'registration/login.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse_lazy('index'))
        else:
            context = {'error_message', 'Sorry, Username/Password Not Found'}
            return render(request, 'registration/login.html', context)

def ArticleDetailView(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'app/article-detail.html', {'article': article})

def ThreadDetailView(request, pk):
    if request.method == 'GET':
        thread = get_object_or_404(Thread, pk=pk)
        comments = thread.comments.all()
        if comments is not None:
            comment_list = comments
        return render(request, 'app/thread-detail.html', {'thread': thread})
    elif request.method == 'POST':
        if request.user.is_authenticated:
            body = request.POST['body']
            email = request.user
            thread = get_object_or_404(Thread, pk=pk)
            if thread is not None:
                comment = Comment(body=body, email=email, thread=thread)
                comment.save()
                return render(request, 'app/thread-detail.html', {'thread': thread})
            else:
                thread_list = get_list_or_404(Thread)
                return render(request, 'app/thread-list.html', {'threads': thread_list})
        else:
            return render(request, 'registration/login.html')

class SignUpForm(generic.CreateView):
    form_class= UserCreateForm
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"

def CreateThreadView(request):
        if request.method == 'GET':
            context = {}
            if request.user.is_authenticated:
                return render(request, 'app/create-thread.html', context)
            else:
                return HttpResponseRedirect(reverse_lazy('login'))
        elif request.method == 'POST':
            if request.user.is_authenticated:
                context = {}
                user = request.user
                title = request.POST['title']
                text = request.POST['text']
                thread = Thread(author=user, title=title, text=text)
                thread.save()
                return HttpResponseRedirect(reverse_lazy('thread_list'))
            else:
                return HttpResponseRedirect(reverse_lazy('login'))


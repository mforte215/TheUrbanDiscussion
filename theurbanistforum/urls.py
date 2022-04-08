
from django.contrib import admin
from django.urls import path, include
from app import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.IndexView, name='index'),
    path('threads/', views.threadListView, name='thread_list'),
    path('threads/<uuid:pk>/', views.ThreadDetailView, name='thread_detail'),
    path('create-thread/', views.CreateThreadView, name='create-thread'),
    path ('login/', views.LoginView, name='login'),
    path('articles/<uuid:pk>/', views.ArticleDetailView, name='article_detail'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('sign-up/', views.SignUpForm.as_view(), name='signup'),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
]

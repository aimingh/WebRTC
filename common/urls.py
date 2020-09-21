

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

#'board' is not a registered namespace
app_name='common' #이렇게 써줘야 없어진다  

urlpatterns = [
    path('', views.home, name="home"),
    path('record', views.index, name="index"),
    path('save', views.save, name="save"), #http://127.0.0.1/save     
    path('start', views.start, name="start"), #http://127.0.0.1/common/save     
    # 로그인 관리
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),  
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
]
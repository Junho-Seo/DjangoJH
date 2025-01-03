from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    # 1. 회원가입
    path('signup/', views.signup, name='signup'),
    # 2. 로그인
    path('login/', views.login, name='login'),
    # 3. 로그아웃
    path('logout/', views.logout, name='logout'),
]
from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    # url 분리 시 빈 리스트라도 urlpatterns는 남겨둘 것
    # 서버 실행 시 include 에러 발생함
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]

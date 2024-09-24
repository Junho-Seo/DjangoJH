from django.urls import path
from . import views

# name이 겹치는 문제를 방지
# books 라는 이름 공간(namespace)를 만드는 것
app_name='books'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'), # 생성
    path('<int:pk>/', views.detail, name='detail'),
    # 경로를 이름으로 호출하기 위해 name 사용
    # 경로가 길거나 변수가 여러개인 경우 유지보수가 힘들기 때문
    path('<int:pk>/update/', views.update, name='update'),# 수정
    path('<int:pk>/delete/', views.delete, name='delete'), # 삭제
]

from django.urls import path
from . import views

app_name="books"
urlpatterns = [
    path('', views.index, name="index"),
    path('create/', views.create, name="create"),  # 생성
    path('<int:pk>/', views.detail, name="detail"),
    path('<int:pk>/update', views.update, name="update"), # 수정
    path('<int:pk>/delete/', views.delete, name="delete"),# 삭제
]

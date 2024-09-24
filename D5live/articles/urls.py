from django.urls import path
from . import views


app_name = 'articles'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.detail, name='detail'),
    path('new/', views.new, name='new'),
    path('create/', views.create, name='create'),
    path('<int:pk>/delete', views.delete, name='delete'),
    # 삭제를 하려면 조회가 먼저 이루어져야 하기 때문에 variable routing 사용
    path('<int:pk>/edit/', views.edit, name='edit'),
    path('<int:pk>/update/', views.update, name='update'),
    # 수정도 마찬가지로 조회 먼저 해야하기 때문에 variable routing 사용

    # url도 작성 권장 순서가 있다. 추후 학습 예정
]

from django.urls import path
# import views  # 나중에 복잡해지면 충돌 가능성이 높다
from . import views  # 앱을 명시하는 것을 권장 (.: 현재 경로)

urlpatterns = [
    path('', views.index),
    path('create/', views.create),
]
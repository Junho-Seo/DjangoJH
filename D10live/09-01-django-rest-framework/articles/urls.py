from django.urls import path
from articles import views

# app_name 과 path name이 없어진 이유
# 이 둘은 DTL의 url 태그에서 사용하기 위해 작성되었지만
# 여기서는 templates를 사용하지 않으므로 필요가 없다.
urlpatterns = [
    path('articles/', views.article_list),
    path('articles/<int:article_pk>/', views.article_detail),
]

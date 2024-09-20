from django.db import models


# 클래스 괄호 안 => (상속받을 상위 클래스; models 모듈 안에 있는 Model 클래스)
# title, content : 클래스 변수
# 클래스인지 메서드인지 구분하는 법: 이름이 대문자면 클래스 (관례)
class Article(models.Model):
  title = models.CharField(max_length=10)
  content = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
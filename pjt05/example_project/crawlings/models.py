from django.db import models

class Article(models.Model):
    query = models.TextField()  # 검색어
    title = models.TextField()  # 결과의 제목들
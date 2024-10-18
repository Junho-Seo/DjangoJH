from django.db import models
from django.conf import settings


# Create your models here.
class Board(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='boards')
    # 실제 개발에서는 on_delete를 어떻게 설정할까?
    # 유저가 지워졌을 때 어떻게 작업할까?
    #   - 아무 행동 안 한다. (유저 탈퇴시 db에서 날리지 않는다.)
    #   - admin으로 변경 (관리자가 관리)
    title = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author_comments')
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='board_comments')
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
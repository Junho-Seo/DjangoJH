from django.db import models


class Book(models.Model):
    isbn = models.CharField(max_length=15, unique=True)  # 도서 번호, 고유값
    description = models.TextField() # 도서 내용
    title = models.CharField(max_length=255)  # 도서 제목
    pub_date = models.DateField()  # 출간 연도
    author = models.CharField(max_length=255)  # 작가
    price_sales = models.DecimalField(max_digits=10, decimal_places=2)  # 판매 가격

    # def __str__(self):
    #     return self.title

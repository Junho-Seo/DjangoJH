from django.db import models

# Create your models here.
class Book(models.Model):
    isbn = models.CharField(max_length=20, unique=True)
    # CharField의 기본값: blank=False, null=False (빈값 허용 x, 없는값 허용 x)
    # blank : 값 자체가 "비어있는 값"
    # null : 데이터가 없다.
    # unique : 고유값(중복 여부)
    title = models.CharField(max_length=255)
    description = models.TextField()
    pub_date = models.DateField()  # 날짜만 저장
    # 시간정보까지 저장하고 싶다면 DateTimeField
    author = models.CharField(max_length=255)
    price_sales = models.DecimalField(max_digits=10, decimal_places=2)
    # 만약 달러로 표시가 되어있다면(소수점 아래 두 자리)
    # 정확한 소수점을 저장할 때 사용하는 필드
    # 정수일 경우 IntegerField()
    
    def __str__(self):
        return f'{self.isbn}: {self.title}'


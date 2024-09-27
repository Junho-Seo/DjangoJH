from django.db import models


# 모델을 생성할 때에는 데이터의 제약조건을 반드시 파악하고 코드를 작성하자
class Weather(models.Model):
   date = models.DateField() # 연도-월-일 형식의 날짜데이터, 결측치는 없음
   temp_avg_f = models.IntegerField() # 정수형, 결측치 없음
   # sqlite3는 리스트 필드가 없다!
   # 전체를 문자열로 저장 후 활용할 때 콤마로 분리(split)
   events = models.CharField(max_length=255, blank=True, null=True)  # 결측치 있음, 1개 이상일 수 있다, 값이 없을 수 있다.
   

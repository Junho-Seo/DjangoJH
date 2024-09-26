from django import forms
from .models import Book

# Form 은 사용자 입력을 받기 위해서 생성
# Form: DB 에 정의된 필드와 관계없는 입력을 추가로 받고 싶을 때
# ModelForm: DB 에 정의된 필드만 사용자 입력으로 받고 싶을 때

# 만약, "몇 권" 이라는 데이터를 추가로 입력받고싶다.
# 권수: DB에는 저장 X, 추가적인 입력만 받고싶다.
# class BookForm(forms.Form):
#     title = forms.CharField(max_length=15)
#     counts = forms.IntegerField()

class BookForm(forms.ModelForm):
    class Meta:
        model = Book  # 어떤 테이블을 기준으로 입력받을 것인가
        # 어떤 필드를 입력받을 것인가
        # 전체 필드를 다 입력받고 싶을 때
        # fields = '__all__'  
        # 원하는 필드만 입력받고 싶을 때 튜플이나 리스트로 작성
        # fields = ('title', 'description', )
        # 특정 필드를 제외하고 입력받고 싶을 때
        exclude = ('external_image', )  # tuple
        # 주의사항. 아래처럼 문자열로 들어가지 않도록 주의!!!
        # exclude = ('author')    # str
        labels = {
            'isbn': '도서 번호',
            'title': '제목',
            'author': '작가',
        }
        widgets = {
            'pub_date': forms.DateInput(attrs={
                'type': 'date',
            }),
            'price_sales': forms.NumberInput(attrs={
                'step': 1,
                'value': 10
            })
        }

from django.shortcuts import render
from .models import Book
import requests
# 알라딘 api 데이터
def get_data():
    API_KEY = "ttbsjh23951131001"
    URL = "http://www.aladin.co.kr/ttb/api/ItemList.aspx"
    params = {
        "ttbkey": "ttbsjh23951131001",
        "SearchTarget": "Book",
        "output": "js",
        "QueryType": "Bestseller",
        "MaxResults": "50",
        "Version": 20131101,
        "start": 1,
    }

    response = requests.get(URL, params=params)
    response = response.json()

    result = []
    for item in response['item']:
        info = {
            'isbn': item['isbn'],
            'title': item['title'],
            'description': item['description'],
            'pubDate': item['pubDate'],
            'author': item['author'],
            'priceSales': item['priceSales'],
        }
        result.append(info)
    return result

# index 페이지 접근 시
# 1. 알라딘 API로 데이터 요청 (50개의 베스트셀러)
#   - 단, 이미 저장된 책이라면 저장하지 않는다.
def index(request):
    data = get_data()
    # data를 반복하면서 이미 저장된 데이터가 아니라면 저장하기
    for item in data:
        # 특정 데이터 존재 여부
        # 1. all 방식
        # python 로직으로 돌아가기 때문에, 많이 느리다.
        # if item['isbn'] not in Book.objects.all():

        # 2. filter 방식 (권장사항: 속도가 더 빠르기 때문에)
        # 검색 기능을 SQL로 변환해서 날리기 때문에, 1. 보다 훨씬 빠르다.
        # .filter(필드명=원하는 값)
        # exists(): 존재 여부
        if not Book.objects.filter(isbn=item['isbn']).exists():
            # 중복이 아닐 경우 새로운 Book 객체 생성
            Book.objects.create(
                isbn = item['isbn'],
                title = item['title'],
                description = item['description'],
                pub_date = item['pubDate'],
                author = item['author'],
                price_sales = item['priceSales'],
            )
  
    # books = Book.objects.all()

    # 필터링 기능 추가
    # 가격 필터링 값 가져오기
    max_price = request.GET.get('max_price')

    # 도서 목록 필터링
    if max_price:
        # price_sales 값이 max_price 보다 작은 데이터들을 조회
        books = Book.objects.filter(price_sales__lte=max_price)
    else:
        books = Book.objects.all()
    
    context = {
        'books': books,
    }

    return render(request, 'books/index.html', context)

def detail(request, pk):
    # pk 가 전달받은 pk 인 book 검색
    book = Book.objects.get(pk=pk)
    context = {
        'book': book,
    }
    # detail.html 랜더링
    return render(request, 'books/detail.html', context)
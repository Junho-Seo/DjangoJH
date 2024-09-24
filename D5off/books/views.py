import requests, json

from django.shortcuts import render, redirect
from .models import Book

flag = 1  # 서버를 다시 시작해야 초기화

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
    global flag
    if flag:
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
    flag = 0
  
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
        'books': books.order_by('-pk'),
        # count(): Book에 저장된 레코드 수를 반환
        'total_count': Book.objects.count(),
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

# 1. POST 요청: 게시글을 생성(DB에 저장)
# 2. GET 요청: 생성 페이지를 출력
def create(request):
    if request.method == 'POST':
        # print('data = ', request.POST)
        info = {
            'isbn': request.POST.get('isbn'),
            'title': request.POST.get('title'),
            'description': request.POST.get('description'),
            'author': request.POST.get('author'),
            'price_sales': request.POST.get('price_sales'),
            'pub_date': request.POST.get('pub_date'),
        }

        # 유효성 검증이 끝났다고 가정
        # dict unpacking: (**)
        
        # create 메서드는 인스턴스를 반환한다.
        book = Book.objects.create(**info)
        # book.title = 'test'
        # # 수정 후 ,DB에 반영하기 위해 save 호출
        # book.save()

        # 생성 완료 후에는 index페이지로 이동
        # return render(request, 'books/index.html')
        # context를 넘겨주지 않아서, 데이터가 보이지 않는다.

        # 해결방안 2가지
        # 첫 번째 방법. context를 그냥 넘겨주자
        #   문제점. URL이 이상하다
        #   전체 데이터를 보는 URL이 두 가지가 되어버린다.
        # books = Book.objects.all()
    
        # context = {
        #     'books': books,
        # }

        # return render(request, 'books/index.html', context)
    
        # 해결 방법
        print('book = ', book)
        return redirect('books:detail', book.pk)
    else:
        return render(request, 'books/create.html')
    
def delete(request, pk):
    # pk 값을 가진 인스턴스 가져오기
    book = Book.objects.get(pk=pk)
    # 삭제
    book.delete()
    # index로 이동 (재요청)
    return redirect('books:index')

def update(request, pk):
    # 기존 데이터를 가져와서 변경
    book = Book.objects.get(pk=pk)
    # POST 요청: 수정하는 로직
    if request.method == "POST":
        book.isbn = request.POST.get('isbn')
        book.title = request.POST.get('title')
        book.description = request.POST.get('description')
        book.author = request.POST.get('author')
        book.price_sales = request.POST.get('price_sales')
        book.pub_date = request.POST.get('pub_date')

        # 변경된 데이터로 반영
        book.save()
        return redirect('books:detail', book.pk)

    # GET 요청: 수정 페이지 출력
    else:
        context = {
            'book': book,
        }
        return render(request, 'books/update.html', context)
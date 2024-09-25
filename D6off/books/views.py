import requests, json

from django.shortcuts import render, redirect
from .models import Book
from .forms import BookForm

flag = 1  # 서버가 최초로 실행될때만 해석

def get_data():
    API_URL = 'http://www.aladin.co.kr/ttb/api/ItemList.aspx'
    API_KEY = 'ttbsjh23951131001'
    params = {
        'ttbkey': API_KEY,
        'QueryType': 'Bestseller',
        'MaxResults': 50,
        'start': 1,
        'SearchTarget': 'Book',
        'output': 'js',
        'Version': 20131101
    }

    response = requests.get(API_URL, params=params)
    response = json.loads(response.text)

    result = []
    for item in response['item']:
        info = {
            'isbn': item['isbn'],
            'title': item['title'],
            'description': item['description'],
            'pubDate': item['pubDate'],
            'author': item['author'],
            'priceSales': item['priceSales']
        }
        result.append(info)
    return result


def index(request):
    global flag
    if flag:
        data_list = get_data()
        for item in data_list:
            # 저장된 데이터가 아니라면 생성
            if not Book.objects.filter(isbn=item['isbn']).exists():
                # 중복이 아닐 경우 새로운 Book 객체 생성
                Book.objects.create(
                    isbn=item['isbn'],
                    title=item['title'],
                    description=item['description'],
                    pub_date=item['pubDate'],
                    author=item['author'],
                    price_sales=item['priceSales']
                )
        flag = 0

    # books = Book.objects.all()

    # 필터링 기능 추가
    # 가격 필터링 값 가져오기
    max_price = request.GET.get('max_price')

    # 도서 목록 필터링
    if max_price:
        books = Book.objects.filter(price_sales__lt=max_price)
    else:
        books = Book.objects.all()
        
    context = {
        'books': books.order_by('-pk'),
        # count(): Book 에 저장된 레코드 수를 반환
        'total_count': Book.objects.count(),
    }
    return render(request, 'books/index.html', context)


def detail(request, pk):
    book = Book.objects.get(pk=pk)
    context = {
        'book': book,
    }
    return render(request, 'books/detail.html', context)


# 1. POST 요청: 게시글을 생성(DB에 저장)
# 2. GET 요청: 생성 페이지를 출력
def create(request):
    if request.method == 'POST':
        # form에 데이터를 채워넣는다.
        form = BookForm(request.POST)
        if form.is_valid():  # 데이터가 정상이라면
            book = form.save()
            return redirect('books:detail', book.pk)
    else:
        form = BookForm()
    context = {
        'form': form,
    }
    return render(request, 'books/create.html', context)
    

def delete(request, pk):
    # pk 값을 가진 인스턴스 가져오기
    book = Book.objects.get(pk=pk)
    # 삭제
    book.delete()
    # index 페이지 이동(재요청)
    return redirect("books:index")

def update(request, pk):
    book = Book.objects.get(pk=pk)
    # POST 요청: 수정하는 로직
    if request.method == 'POST':        
        # 기존 데이터를 가져와서 변경
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("books:detail", book.pk)

    # GET 요청: 수정 페이지 출력
    else:
        form = BookForm(instance=book)
    context = {
        'book': book,
        'form': form,
    }
    return render(request, 'books/update.html', context)
    
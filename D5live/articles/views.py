from django.shortcuts import render, redirect
# 모델 클래스 가져오기
from .models import Article

# Create your views here.
def index(request):
    # 게시글 전체 조회 요청 to DB
    articles = Article.objects.all()
    context = {
        'articles': articles,
    }
    return render(request, 'articles/index.html', context)

def detail(request, pk):
    # url로부터 전달받은 pk를 이용해 데이터를 조회해야한다.
    # 오른쪽 pk는 인자로 넘어온 pk
    # 왼쪽 pk는 Article 모델의 id 필드
    # article = Article.objects.get(id=pk)
    article = Article.objects.get(pk=pk)
    context = {
        'article': article
    }
    return render(request, 'articles/detail.html', context)

def new(request):
    # 사용자에게 게시물 작성 페이지 응답
    return render(request, 'articles/new.html')

# 지난 수업의 catch
def create(request):
    # 1. 사용자 요청으로부터 입력 데이터를 추출
    title = request.POST.get('title')
    content = request.POST.get('content')
    # 데이터 저장 방법 1
    # 굳이 필터를 하나씩 다 써야한다.
    # article = Article()
    # article.title = title
    # article.content = content
    # article.save()

    # 데이터 저장 방법 2 (선택 방법)
    # 유효성 검사(보안 검사)가 가능하며 코드를 짧게 작성 가능
    article = Article(title=title, content=content)
    article.save()

    # 데이터 저장 방법 3
    # 유효성 검사를 진행할 타이밍이 없다. (저장 전)
    # 물론 사용할 일이 없는 것은 아니지만 오래 사용할 방법은 2번
    # Article.objects.create(title=title, content=content)

    # 3. 추출한 입력 데이터를 활용해 DB에 저장 요청
    # return render(request, 'articles/create.html')
    # return redirect('articles:index')  # 메인 화면으로 재요청
    return redirect('articles:detail', article.pk)

def delete(request, pk):
    # 어떤 게시글을 삭제할지 조회
    article = Article.objects.get(pk=pk)
    # 조회한 게시글 삭제
    article.delete()
    return redirect('articles:index')

def edit(request, pk):
    # 어떤 게시글을 수정할지 조회
    article = Article.objects.get(pk=pk)
    context = {
        'article': article,
    }
    return render(request, 'articles/edit.html', context)

def update(request, pk):
    # 1. 수정할 게시글 조회
    article = Article.objects.get(pk=pk)
    # 2. 사용자로부터 받은 새로운 입력 데이터 추출
    title = request.POST.get('title')
    content = request.POST.get('content')
    # 3. 기존 게시글의 데이터를 사용자로 받은 데이터로 새로 할당
    article.title = title
    article.content = content
    # create view 함수와의 차이점: 수정을 위해 조회를 먼저 시작
    # 4. 저장
    article.save()

    return redirect('articles:detail', article.pk)
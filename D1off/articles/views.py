# render: html을 완성해서(화면을 그려서) return
from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def index(request):
    # return JsonResponse({'message':'test'})
    # articles/index.html 인 이유
    # 앱이 여러 개일 때, articles 폴더 하위에 있는
    # html 파일이라는 것을 명시하기 위해
    # 디렉토리를 구분지어 준다.
    return render(request, 'articles/index.html')

def article(request):
    return render(request, 'articles/article.html')
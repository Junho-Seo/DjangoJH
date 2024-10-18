from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Article
from .serializers import ArticleListSerializer, ArticleSerializer

# DRF의 기본 규칙(약속): api_view 데코레이터를 사용해야만 DRF 사용 가능
@api_view(['GET', 'POST'])
def article_list(request):
    if request.method == "GET":
        # 전체 게시글 조회 (타입: queryset, 장고에서 사용하는 데이터 타입)
        article = Article.objects.all()
        # 변환하기 쉬운 포멧으로 전환 (직렬화)
        serializer = ArticleListSerializer(article, many=True)
        # 쿼리셋은 다중 데이터이므로 many 옵션 추가 (단일 데이터일 때는 필요 없는 옵션)
        return Response(serializer.data)
        # serializer는 변환된 덩어리다. 여기서 데이터만 추출 (serializer.data)
    
    # elif 사용 이유
    # method가 4가지가 되었기 때문에 명시를 위해
    elif request.method == 'POST':
        # ModelSerializer를 사용해 사용자 입력 데이터를 받아 직렬화 진행
        # 모델폼과 다른 부분: (data=request.POST)
        serializer = ArticleSerializer(data=request.data)
        # 유효성 검사
        # is_valid, save 메서드 모두 ModelForm의 것과 동일 구조(동일 이름)
        # 이는 DRF 개발진이 구성을 동일하게 맞춘 것 뿐이며 내부 코드는 ModelForm의 것과는 전혀 다르다.
        if serializer.is_valid():
            serializer.save()
            # 저장 성공 후 201 응답 상태코드 반환
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # 유효성 검사 실패 후 400 응답 상태코드 반환
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'DELETE', 'PUT'])
def article_detail(request, article_pk):
    article = Article.objects.get(pk=article_pk)

    if request.method == "GET":
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    
    elif request.method == "DELETE":
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    elif request.method == 'PUT':
        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

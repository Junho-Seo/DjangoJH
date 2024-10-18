from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Article, Comment
from .serializers import ArticleListSerializer, ArticleSerializer, CommentSerializer


@api_view(['GET', 'POST'])
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'DELETE', 'PUT'])
def article_detail(request, article_pk):
    article = Article.objects.get(pk=article_pk)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        serializer = ArticleSerializer(
            article, data=request.data, partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


@api_view(['GET'])
def comment_list(request):
    if request.method == 'GET':
        # 댓글 전체 조회
        comments = Comment.objects.all()
        # 댓글 목록 쿼리셋을 직렬화
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


@api_view(['GET', 'DELETE', 'PUT'])
def comment_detail(request, comment_pk):
    # comment = Comment.objects.get(pk=comment_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)
    # GET method의 특징(복습)
    #   1. 조회한 객체가 없을 때 DOESNOTEXIST 예외 발생
    #   2. 조회한 객체가 2개 이상일때 Multple... 예외 발생
    # 서버는 예외가 발생하면 코드가 중단된다! (500)
    # 해결책
    #   - 예외 처리 (try except)
    #     하지만 GET메서드는 자주 사용되기 때문에 매번 try except를 작성하기 번거로움
    #   - django에서는 반복을 줄이기 위해 DOESNOTEXIST 자동으로 캐치해 404를 응답해주는 메서드 제공

    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            # 수정 시에는 외래 키 데이터 필요 없음
            # 이미 외래키가 들어있는 댓글을 내용만 수정하기 때문
            serializer.save()
            return Response(serializer.data)


@api_view(['POST'])
def comment_create(request, article_pk):
    # 게시글 조회 (어떤 게시글에 작성되는 댓글인지)
    article = Article.objects.get(pk=article_pk)
    # 사용자 입력 데이터 직렬화 (사용자가 입력한 댓글 데이터)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        # 외래 키 데이터 입력 후 저장
        # 모델 폼의 경우는 commit=False를 이용하여 save 전에 인스턴스 생성 후 저장했었다.
        # 좌변 article: Comment 모델의 article 필드
        # 우변 article: 위의 단일 객체 조회 변수명 article
        serializer.save(article=article)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

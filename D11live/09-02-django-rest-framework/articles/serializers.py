from rest_framework import serializers
from .models import Article, Comment


class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = (
            'id',
            'title',
            'content',
        )


class ArticleSerializer(serializers.ModelSerializer):
    class CommentDetailSerializer(serializers.ModelSerializer):
        class Meta:
            model = Comment
            fields = ('id', 'content',)
    
    # comment_set 역참조 데이터를 override
    #   ArticleSerializer 입장에서 CommentDetailSerializer의 결과는 다중데이터(쿼리셋)
    #   따라서 many 옵션 추가
    #   키워드 인자로 넣기 때문에 순서는 상관 없음
    #   역참조 변수 명을 변경하고 싶다면?
    #       1. models.py의 Comment 클래스에 related_name= 속성 추가(기존 역참조 이름 변경 방식)
    #       2. 이후 아래의 comment_set(기존 이름)을 변경된 이름으로 수정
    comment_set = CommentDetailSerializer(read_only=True, many=True)
    # 댓글 개수 제공을 위한 새로운 필드 생성
    #   역참조와 다르게 원하는 변수명 사용 가능
    #   serializers의 필드 명의 경우는 DRF 공식 문서 참조(Django의 필드 명과는 다를 수 있음)
    #   유효성 검사에 들어가기 때문에 read_only 옵션 추가
    number_of_comments = serializers.IntegerField(source='comment_set.count', read_only=True)
    #   기존에 사용한 댓글의 개수 세는 법 article.comment_set.count()
    #   article 인스턴스가 삭제된 이유
    #       ArticleSerializer(override할 클래스)가 Article로 인해 만들어진 Serializer이기 때문에 생략(문법적인 내용)


    class Meta:
        model = Article
        fields = '__all__'



class CommentSerializer(serializers.ModelSerializer):
    class ArticleTitleSerializer(serializers.ModelSerializer):
        class Meta:
            model = Article
            fields = ('title',)
    # 기존 article 데이터 값을 override
    # 그런데 기존 필드를 override 하게되면 오버라이드 할 클래스 안의 Meta클래스의 read_onlyfields를 사용할 수 없다.(교안참고)
    # 이를 보정하기 위해 ModelSerializer의 read_only 인자 값으로 재설정
    article = ArticleTitleSerializer(read_only=True)

    class Meta:
        model = Comment
        # fields에 작성된 필드는 모두 유효성 검사 목록에 포함됨
        fields = '__all__'
        # 외래 키 필드를 "읽기 전용 필드"로 지정
        # 이유는? 외래 키 데이터는
        #   1. 유효성 검사에서는 제외하고
        #   2. 결과 데이터에는 포함하고 싶음
        # read_only_fields = ('article',)
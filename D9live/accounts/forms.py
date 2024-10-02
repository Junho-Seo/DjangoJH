from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# django는 아래 처럼 User 모델을 직접 참조하는 것을 권장하지 않는다.
# from .models import User  /   model = User
# 여러 이유가 있지만 기본적으로 유지보수가 힘들다 (모델의 이름이 바뀌거나 다른 모델로 대체하는 경우 등)
# 그래서 django는 User 모델을 간접적으로 참조할 수 있는 방법을 별도로 제공한다.
from django.contrib.auth import get_user_model  # 현재 활성화된 User 객체를 '자동으로' 참조하여 반환하는 함수

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()

class CustomUserChangeForm(UserChangeForm):
    # password = None  비밀번호 설정 관련 안내 출력 숨기기
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email',)
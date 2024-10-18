from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    # 모델 속성을 제외하고 나머지는 모두 Meta 클래스 내용을 그대로 가져오면 된다.
    # 아래처럼 Meta class도 상속받아 사용해도 된다.
    class Meta(UserCreationForm.Meta):
        model = get_user_model()

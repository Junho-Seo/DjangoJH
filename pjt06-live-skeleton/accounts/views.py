from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm


# 기능 하나씩 완성 후 테스트하며 진행하는 습관 들이기
# 기능을 모두(signup, login) 완성 후 테스트했을 때 앞쪽에 문제가 생기면 디버깅이 어렵다.
@require_http_methods(["GET", "POST"])
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # 회원가입 후 바로 로그인
            auth_login(request, user)
            return redirect('boards:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)

@require_http_methods(["GET", "POST"])
def login(request):
    if request.method == 'POST':
        # ModelForm과 Form의 차이: Form은 model 필드 외의 데이터도 입력 가능
        # AuthenticationForm은 forms.Form 상속
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            # next가 있다면, next 경로로 보내라
            # ~/? 뒤로 오는 건 url과 관련 -> POST 요청이어도 GET 안에 들어있다.
            # url 관련 내용은 모두 GET 요청 안에 있다. 주의.
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect("boards:index")
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)
    

@require_http_methods(["POST"])
def logout(request):
    auth_logout(request)
    return redirect('boards:index')
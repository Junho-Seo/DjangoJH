from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required


def signup(request):
    if request.user.is_authenticated:
        return redirect("books:index")
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("books:index")
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


# 로그인 - 데이터 검증, 세션 ID 생성+저장, 사용자에게 세션ID 전달
# -> 복잡하다. 해당 기능들은 django에 함수로 만들어져있다!
def login(request):
    if request.user.is_authenticated:
        return redirect("books:index")
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())

            # 다음 경로가 있다면 해당 경로로 이동
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            
            return redirect("books:index")
    else:
        form = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)


# 로그아웃 - 세션 id 삭제(POST 요청)
def logout(request):
    auth_logout(request)
    return redirect("books:index")

from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from .models import Board, Comment
from .forms import BoardForm, CommentForm
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

# Create your views here.
@require_http_methods(["GET"])
def index(request):
    # 어느 것이 더 좋은 방법? or 언제 사용해야 할까?
    # get_list_or_404: 데이터가 없을 때 404 에러를 띄워준다
    #   - 데이터가 없어도 화면측에서 사용자에게 알림을 줄 수 있다면 사용가능
    #   - 프론트 측(Django에서는 templates)에서 404 error를 처리해줬다면 사용
    # boards = get_list_or_404()
    #   에러를 안띄웠다면 order_by 적용
    # boards = boards.order_by('-created_at')

    # 기본 코드 (데이터가 없다면 빈 리스트 출력)
    # django ORM -> SQL 변환: showmigrations, sqlmigrate 명령어 찾아보기(manage.py)
    boards = Board.objects.all().order_by('-created_at')
    context = {
        'boards': boards
    }
    return render(request, 'boards/index.html', context)

@require_http_methods(["GET", "POST"])
def detail(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        board.delete()
        return redirect('boards:index')

    comments = board.comments.all()
    comment_form = CommentForm()
    
    context = {
        'board': board,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'boards/detail.html', context)

@require_http_methods(["GET", "POST"])
def update(request, pk):
    board = get_object_or_404(Board, pk=pk)

    if request.method == 'POST':
        form = BoardForm(request.POST, instance=board)
        if form.is_valid():
            form.save()
            return redirect('boards:detail', board.pk)
    else:
        form = BoardForm(instance=board)
    context = {
        'board': board,
        'form': form,
    }        
    return render(request, 'boards/update.html', context)

# 데코레이션도 진행 순서에 따라 배치
@login_required
# login required의 장점: 로그인 후 이전에 보고있던 페이지로 redirect해준다.(사용자 경험)
@require_http_methods(["GET", "POST"])
def create(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('boards:index')
    else:
        form = BoardForm()
    context = {
        'form': form,
    }
    return render(request, 'boards/create.html', context)

@require_http_methods(["POST"])
def comment(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.board = board
            comment.save()
            return redirect('boards:detail', board.pk)

@require_http_methods(["POST"])
def comment_detail(request, board_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == 'POST':
        comment.delete()
        return redirect('boards:detail', board_pk)
from django.shortcuts import render, redirect
from .models import Movie
from .forms import MovieForm

# 전체 영화 데이터 조회 GET
def index(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies,
    }
    return render(request, 'movies/index.html', context)

# 영화 데이터 작성 폼 출력 GET
# 유효성 검증 및 영화 데이터 저장 POST
def create(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save()
            return redirect('movies:detail', movie.pk)
    else:
        form = MovieForm()
    context = {
        'form': form,
    }
    return render(request, 'movies/create.html', context)


#단일 영화 데이터 (및 댓글 목록 조회) GET
def detail(request, pk):
    movie = Movie.objects.get(pk=pk)
    context = {
        'movie': movie,
    }
    return render(request, 'movies/detail.html', context)

# 영화 데이터 수정 페이지 조회 GET
# 유효성 검증 및 영화 데이터 수정 POST
def update(request, pk):
    movie = Movie.objects.get(pk=pk)
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movies:detail', movie.pk)
    else:
        form = MovieForm(instance=movie)
    context = {
        'movie': movie,
        'form': form,
    }
    return render(request, 'movies/update.html', context)


# 단일 영화 데이터 삭제 POST
def delete(request, pk):
    movie = Movie.objects.get(pk=pk)
    movie.delete
    return redirect('movies:index')

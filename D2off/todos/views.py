from django.shortcuts import render

# Create your views here.
my_todos = [
    {
        'id': 1,
        'title': 'mm끄기',
        'content': '수업집중',
        'isDone': True
    },
    {
        'id': 2,
        'title': '자소서 쓰기',
        'content': '싸탈하자',
        'isDone': False
    },
    {
        'id': 3,
        'title': '퇴근하기',
        'content': '집에 가야한다',
        'isDone': False
    }
]

def index(request):
    context = {
        'todos': my_todos,
    }
    return render(request, 'todos/index.html', context)

def create(request):
    # POST 요청은 데이터를 생성한다.
    if request.method == 'POST':
        # print(request.POST)
        title = request.POST.get('title')
        content = request.POST.get('content')
        # 체크박스 체크 여부를 True False로 관리
        is_done = request.POST.get('isDone') == 'on'

        new_todo = {
            'id': len(my_todos) + 1,
            'title': title,
            'content': content,
            'isDone': is_done,
        }

        my_todos.append(new_todo)

        context = {
          'todos': my_todos,
        }
        return render(request, 'todos/index.html', context)
        
    # GET요청은 페이지를 보여준다.,
    return render(request, 'todos/create.html')
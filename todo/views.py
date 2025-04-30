from django.shortcuts import render
from django.http import Http404
from todo.models import Todo
from config.fake_db import user_db

_db = user_db

def todo_list(request):
    todo_list = Todo.objects.all().values_list('id','title')
    result = [{'id': todo[0], 'title': todo[1]} for i, todo in enumerate(todo_list)]

    return render(request, 'todo_list.html', {'data': result})


def todo_info(request, todo_id):
    try:
        todo = Todo.objects.get(id=todo_id)
        info = {
            'title': todo.title,
            'description': todo.description,
            'start_date': todo.start_date,
            'end_date': todo.end_date,
            'is_completed': todo.is_completed,
        }
        return render(request, 'todo_info.html', {'data': info})
    except Todo.DoesNotExist:
        raise Http404("Todo does not exist")

def user_list(request):
    names = [{'id': key, 'name': value['이름']} for key, value in _db.items()]
    return render(request, 'user_list.html', {'names': names})

def user_info(request, user_id):
    if user_id > len(_db):
        raise Http404('유저를 찾을 수 없습니다.')
    info = _db[user_id]
    return render(request, 'user_info.html', {'info': info})
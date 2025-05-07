
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from todo.forms import TodoForm, TodoUpdateForm #Form 파일 생성 잊지 말기~
from todo.models import Todo
from config.fake_db import user_db

_db = user_db

def todo_list(request):
    todo_list = Todo.objects.all().values_list('id','title')
    result = [{'id': todo[0], 'title': todo[1]} for i, todo in enumerate(todo_list)]

    return render(request, 'todo/todo_list.html', {'data': result})


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
        return render(request, 'todo/todo_info.html', {'data': info})
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

@login_required()
def todo_create(request):
    form = TodoForm(request.POST or None)
    if form.is_valid():
		     # form으로부터 넘겨받은 데이터를 바탕으로 Todo 객체를 저장
		     # 데이터베이스에 저장하기전 user 정보를 추가하기위해 commit=False 를 사용
        todo = form.save(commit=False)
        todo.user = request.user # Todo 객체에 user정보를 추가
        todo.save() # user정보가 추가된 Todo 객체를 데이터베이스에 저장
    return redirect(reverse('todo_info', kwargs={'todo_id': todo.pk}))
    context = {
        'form': form
    }
    return render(request, 'todo/todo_create.html', context)


@login_required()
def todo_update(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    form = TodoUpdateForm(request.POST or None, instance=todo)
    if form.is_valid():
        form.save()
        return redirect(reverse('todo_info', kwargs={'todo_id': todo.pk}))
    context = {
        'form': form
    }
    return render(request, 'todo/todo_update.html', context)


@login_required()
def todo_delete(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    todo.delete()
    return redirect(reverse('todo_list'))
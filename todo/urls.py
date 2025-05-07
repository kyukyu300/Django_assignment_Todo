from django.urls import path
from .cb_views import TodoListView, TodoCreateView, TodoDetailView, TodoUpdateView, TodoDeleteView
urlpatterns = [
    path('cbv/todo/', TodoListView.as_view(), name='cbv_todo_list',),
    path('cbv/todo/create/', TodoCreateView.as_view(), name='cbv_todo_create'),
    path('cbv/todo/<int:pk>/', TodoDetailView.as_view(), name='cbv_todo_info'),
    path('cbv/todo/<int:pk>/update/', TodoUpdateView.as_view(), name='cbv_todo_update'),
    path('cbv/todo/<int:pk>/delete/', TodoDeleteView.as_view(), name='cbv_todo_delete'),
]
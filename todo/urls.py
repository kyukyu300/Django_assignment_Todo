from django.urls import path, include
from .cb_views import TodoListView, TodoCreateView, TodoDetailView, TodoUpdateView, TodoDeleteView, CommentCreateView, CommentDeleteView, CommentUpdateView
urlpatterns = [
    path('cbv/todo/', TodoListView.as_view(), name='cbv_todo_list',),
    path('cbv/todo/create/', TodoCreateView.as_view(), name='cbv_todo_create'),
    path('cbv/todo/<int:pk>/', TodoDetailView.as_view(), name='cbv_todo_info'),
    path('cbv/todo/<int:pk>/update/', TodoUpdateView.as_view(), name='cbv_todo_update'),
    path('cbv/todo/<int:pk>/delete/', TodoDeleteView.as_view(), name='cbv_todo_delete'),
    path('comment/<int:todo_id>/create/',  CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:pk>/delete/',  CommentDeleteView.as_view(), name='comment_delete'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment_update'),
    path('summernote/', include('django_summernote.urls')),
]
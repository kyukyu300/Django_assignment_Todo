"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.http import Http404
from django.shortcuts import render
from django.urls import path
from config.fake_db import user_db

_db = user_db

def user_list(request):
    names = [{'id': key, 'name': value['이름']} for key, value in _db.items()]
    return render(request, 'user_list.html', {'names': names})

def user_info(request, user_id):
    if user_id > len(_db):
        raise Http404('유저를 찾을 수 없습니다.')
    info = _db[user_id]
    return render(request, 'user_info.html', {'info': info})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("user/", user_list, name="user_list"),
    path("user/<int:user_id>/", user_info, name="user_info"),
]

"""
URL configuration for todo_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
# 앱의 views를 직접 가져오는 방식은 앱이 여러 개가 된다면, 유지보수가 매우 힘들다.
#   => include 사용

urlpatterns = [
    path('admin/', admin.site.urls),
    path('todos/', include('todos.urls')),
]
"""myboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path,include
from django.conf import settings #현재 프로젝트의 settings.py를 의미
from django.conf.urls.static import static
# from board.views import home


# localhost:8000으로 왔을때 board로 연결하기 위해 views의 home을 import
urlpatterns = [
    path('',include('common.urls')), #왜 여기 myboard/urls.py에서 작성하는 이유? board/urls.py와의 차이
    path("admin/", admin.site.urls),
    path("board/", include('board.urls')),
]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
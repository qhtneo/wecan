# common/urls.py
from django.urls import path 

# settings.py에 기본으로 있음 로그인 관련
from django.contrib.auth import views as auth_view
# from. =현재폴더에서 
# 현재폴더에서 views.py를 가지고오는데 그ㅇ름이 common_view다
from . import views as common_view

app_name= 'common'

urlpatterns=[
    path('',common_view.index, name='index'),
    # 로그인
    path('login/',auth_view.LoginView.as_view(template_name ='common/login.html'), name= 'login'),
    # 로그아웃
    path('logout/',auth_view.LogoutView.as_view(), name = 'logout'),
    # 회원 가입
    path('signup/',common_view.signup_custom,name = 'signup'),
    # 회원 삭제
    path('delete/',common_view.delete, name ='delete'),
    # 회원 수정
    path('update/',common_view.update, name ='update'),
    
    path('mypage/',common_view.mypage, name ='mypage'),

    # 회원가입 v1
    # path('signup/',common_view.signup),
    
]
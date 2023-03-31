from django.urls import path
from . import views

app_name ='board'

#여기는 board에 있는 urls.py다
urlpatterns = [

    # .../board
    path('', views.index, name = 'index'),
    # 글읽기 주소 /board/0
    path('<int:id>/',views.read, name='detail'),
    # 글쓰기 주소
    path('write/',views.write, name='write'),
    # 수정 주소
    path('<int:id>/update/',views.update, name ='update'),
    # 삭제 주소
    path('<int:id>/delete/',views.delete, name ='delete'),
    
    # #AJAX
    # path('callAjax/',views.call_ajax),
    # 댓글 쓰기 주소
    path('write_reply/',views.write_reply),
    # 댓글 수정 주소
    path('update_reply/',views.update_reply),
    # 댓글 로딩 주소
    path('load_reply/',views.load_reply),
    # 댓글 삭제 주소
    path('delete_reply/',views.delete_reply),

]
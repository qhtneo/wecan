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
    path('<int:id>/write_reply/',views.write_reply, name = "write_reply"),
    # 댓글 수정 주소
    path('<int:id>/update_reply/',views.update_reply, name = "update_reply"),
    # 댓글 로딩 주소
    path('<int:id>/load_reply/',views.load_reply, name = 'load_reply'),
    # 댓글 삭제 주소
    path('<int:id>/delete_reply/',views.delete_reply, name = "delete_reply"),
    path("<int:id>/download/",views.download, name = "download"),

    # CBV방식으로 호출할 주소 cbv라는 글자가 붙어있으면 호출
    # as_view : 클래스를 view의 기능으로 사용하겠다.
    path('cbv/', views.BoardList.as_view()),
    path('cbv/<int:id>/', views.BoardDetail.as_view()),
]
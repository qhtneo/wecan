from django.urls import path
from . import views

#d여기는 order에 있는 urls.py
urlpatterns =[
    path('',views.index),
    path('add_order/',views.order),
    path('list_order/',views.list_order),
    path('search_order/',views.search_order),
    path('<int:id>/',views.read),
    path('<int:id>/delete/',views.delete),
    path('<int:id>/update/',views.read),
]
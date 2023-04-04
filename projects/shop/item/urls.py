from django.urls import path
from . import views

app_name = "item"

urlpatterns = [
    path('',views.index,name='index'),
    path('add_item/',views.add_item, name='add_item'),
    path('item_list/',views.item_list, name='item_list'),
    path('search_item/',views.search_item),
    path('add_order/',views.add_order, name = "add_order"),
    path('<int:id>/update_item/',views.update_item, name = "update_item"),
    path('<int:id>/delete_item/',views.delete_item, name ="delete_item"),
    
    path('cbv/', views.OrderList.as_view(),name = "cbv"),
]

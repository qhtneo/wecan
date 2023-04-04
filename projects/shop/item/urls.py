from django.urls import path
from . import views

app_name = "item"

urlpatterns = [
    path('',views.index,name='index'),
    path('addItem/',views.add_item, name='addItem'),
    path('itemList/',views.item_list, name='itemList'),
    path('searchItem/',views.search_item),
    path('addOrder/',views.addOrder,name = "addOrder"),
    path('<int:id>/update_item/',views.update_item, name = "update_item"),
    path('<int:id>/delete_item/',views.delete_item,name ="delete_item"),
    
    path('cbv/', views.OrderList.as_view(),name = "cbv"),
]

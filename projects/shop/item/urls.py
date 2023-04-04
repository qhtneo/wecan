from django.urls import path
from . import views

app_name = "item"

urlpatterns = [
    path('',views.index,name='index'),
    path('addItem/',views.add_item, name='addItem'),
    path('itemList/',views.item_list, name='itemList'),
    path('searchItem/',views.search_item),
    path('addOrder/',views.add_order,name = "addOrder"),

]

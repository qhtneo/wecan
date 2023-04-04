from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse,FileResponse
from .models import Item,Order
from django.views.generic import ListView,DetailView
# Create your views here.
def index(request):
    return render(request,'item/index.html')

# 상품 추가해주는 함수
def add_item(request):
    if request.method=="POST":
        item_name = request.POST['item_name']
        item_count = request.POST['item_count']
        item =  Item(
            item_name = item_name,
            item_count = item_count # user객체 저장
        )
        item.save()
        return HttpResponseRedirect('/item/')
    else:
        return render(request,'item/addItem.html')
    
# 상품 리스트 보내주는 함수
def item_list(request):
    result = Item.objects.all()
    result = result.order_by("-id")
    # 모든 상품을 item_list로 보내줌
    return render(request,'item/itemList.html', {'item_list':result})

# 상품 검색
def search_item(request):
    item_name = request.GET['item_name']
    # 상품 이름을 포함하는 검색
    result = Item.objects.filter(item_name__contains = item_name)
    result = result.order_by("-id")
    return render(request,'item/itemList.html', {'item_list':result})

# 주문 추가
def addOrder(request):
    if request.method =="POST":
        # 주문 수량을 가져온다
        quantity = request.POST['quantity']
        item = Item.objects.get(id=request.POST['optid'])
        order = Order(
            item = item,
            quantity = quantity
        )
        order.save()
        return HttpResponseRedirect("/item/")
        
    # get 방식으로 item리스트를 모두 받아옴    
    else:
        items = Item.objects.all()
        if request.GET:
            id = request.GET['id']
            item = Item.objects.get(id = id)
            item_count = item.item_count
            return JsonResponse({"item_count":item_count})
        #  아이템을 담아서 쏴줌
        return render(request,"item/addOrder.html",{'items': items})
    
def update_item(request,id):
    if request.method =="POST":
        print("id =",id)
        print(request.POST['item_name'])
        print(request.POST['item_count'])
        item  = Item.objects.get(id=id)
        item.item_name=request.POST['item_name']
        item.item_count=request.POST['item_count']
        item.save()
        return HttpResponseRedirect('/item/itemList/')
    else:
        print("id:",id)
        items = Item.objects.get(id = id)
        return render(request,"item/updateItem.html",{'items': items})

def delete_item(request,id):
    Item.objects.get(id=id).delete()
    return HttpResponseRedirect('/item/itemList/')

class OrderList(ListView):
    model = Order
    ordering = '-id'
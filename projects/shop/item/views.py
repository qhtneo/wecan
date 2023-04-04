from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse,FileResponse
from .models import Item,Order
# Create your views here.
def index(request):
    return render(request,'item/index.html')
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

def item_list(request):
    result = Item.objects.all()
    result = result.order_by("-id")
    return render(request,'item/itemList.html', {'item_list':result})

def search_item(request):
    item_name = request.GET['item_name']
    result = Item.objects.filter(item_name__contains = item_name)
    result = result.order_by("-id")
    return render(request,'item/itemList.html', {'item_list':result})

def add_order(request):
    if request.method =="POST":
        print("post방식")
        quantity = request.POST['quantity']
        print("주문수량은:",quantity)
        # item = request.POST['itemName']
        # print("제품명은",item)
        # item = request.POST['item']
        # quantity =request.POST['quantity']
        # order =  Order(
        #     item = item,
        #     quantity = quantity # user객체 저장
        # )
        # order.save()
        pass
        # return HttpResponseRedirect("/item/")
    else:
        items = Item.objects.all()
        context = {'items': items}
        return render(request,"item/addOrder.html",context)

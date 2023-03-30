from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Order
# Create your views here.
def index(request):
    print('index() 실행')
    # return render(request,'board/index.html')
    # 반환되는 queryset에 대해서 order_by함수 이용하면 특정 필드 기준으로 정렬
    # order_by에 들어가는 필드 앞에 -를 붙이면 내림차순(desc) 아니면 오름차순

    Order_list = Order.objects.all().order_by('-id')
    
    context ={
        'Order_list':Order_list
    }
    return render(request,'order/index.html', context)

def home(request):
    # 목록으로
    return HttpResponseRedirect("/order/")

def order(request):
    if request.method =='GET': #요청방식이 get 방식이면 화면 표시
        return render(request,'order/add_order.html')
    else:
        order_text = request.POST['product_name']
        price = request.POST['price']
        address = request.POST['address']
        print("등록 완료",order_text,price,address)
        Order.objects.create(
            order_text = order_text,
            price = price, #세션에 있는 값 저장
            address = address
        )
        return HttpResponseRedirect('/order/')

def list_order(request):
    # result = None # 필터링 된 리스트
    # context = {}

    # # print(request.GET)
    # #검색 조건과 검색 키워드가 있어야 필터링 실행
    # if 'searchType' in request.GET and 'searchWord' in request.GET:
    #     search_type = request.GET['searchType'] # get안의 문자열은 
    #     search_word = request.GET['searchWord'] # html의 name속성과 일치해야함
    #     print("searchType :{}, search_word : {}".format(search_type,search_word))
    # order = Order.objects.all().order_by('id')
    context = {
        "order_list" : order
    }
    return render(request,'order/list_order.html',context)

# def search_order(request):
#     search_name = request.POST['product_name']
#     check = request.POST['check']

#     if check == 'order_text':
#         order_list=Order.objects.filter(order_text__contains = search_name)
#     else:
#         order_list=Order.objects.filter(address__contains = search_name)
#     context={
#         'order_list':order_list
#     }
#     return render(request,'order/list_order.html',context)

def search_order(request):
    input_name = request.POST['product_name']
    check = request.POST['option']
    
    oList = []
    if check =="order":
        oList = Order.objects.filter(order_text__contains = input_name)
    elif check =="front_add":
        oList = Order.objects.filter(address__startswith = input_name)
    elif check =="address":
        oList = Order.objects.filter(address__contains = input_name)
    elif check =="price":
        oList = Order.objects.filter(price__contains  = input_name)
    
    return render(request,"order/list_order.html",{'order_list' : oList})

def read(request,id):
    print("read실행")
    order = Order.objects.get(id = id)
    context ={
        'order':order,
        'oList' : order.order_text.split(",")   
    }
    return render(request,'order/read.html', context)

def delete(request,id):
    Order.objects.get(id=id).delete()
    return HttpResponseRedirect('../../list_order')

def update(request,id):
    order = Order.objects.get(id = id)
    if request.method == "GET":
    #id로 찾은 친구 정보를 템플릿에 표시하기 위해서 
        print("method>>",request.method)
        context = {'order' : order}
        return render(request,'../update_order.html', context)
    else:
        # id로 찾은 객체에 대해서 폼의 값으로 원래 객체의 값 덮어쓰기
        print("method>>",request.method)
        order.order_text = request.POST['order_text']
        order.price = request.POST['price']
        order.address = request.POST['address']
            
        order.save()
        #수정 후에 해당 글로 다시 이동
        redirect_url = '/order/' +str(id) +'/'
        
        return HttpResponseRedirect(redirect_url)
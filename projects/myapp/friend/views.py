from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Friend
# Create your views here.
def index(request):
    print("index 실행됨")
    t = loader.get_template('friend/index.html')
    context={}
    # 응답객체안에 템플릿과 표시할 값(context), 요청(request)
    return HttpResponse(t.render(context,request))  

def add_friend(request):
    print(request.method)
    
    context={}
    t = loader.get_template('friend/friendForm.html')
    # 요청방식이 GET 방식이라면
    if request.method == "GET":
        return HttpResponse(t.render(context,request))
    # 요청방식이 POST 방식이라면
    else :
        # 요청객체에서 값을 가져온다
        name = request.POST['friend_name']
        age = request.POST['friend_age']
        bigo = request.POST['friend_bigo']

        print(name,age,bigo)
        # save()
        f = Friend(
            friend_name = name,
            friend_age = age,
            friend_bigo = bigo
        )
        f.save()
        # 템플릿 반환 방식(단축) render(요청, 템플릿 경로[, context])
        # return render(request, 'friend/index.html')
        return HttpResponseRedirect('/friend/')


def create_friend(request): #request는 항상 들어옴
    name = request.POST['friend_name']
    age = request.POST['friend_age']
    bigo = request.POST['friend_bigo']

    Friend.objects.create(
        friend_name =name,
        friend_age = age,
        friend_bigo = bigo
    )
    # 단축방식을 index.html rendering
    # return render(request,'friend/index.html')
    return HttpResponseRedirect('/friend/show_all')

def show_all(request):
    fList = Friend.objects.all()

    context ={
        'fList':fList
    }
    return render(request,'friend/friend_list.html', context)


def find_name(request):

    name = request.POST['searchName']
    print(name)
    
    fList = Friend.objects.filter(friend_name__contains = name) 
    print(fList)

    context = {
        'fList' : fList
    }
    return render(request, 'friend/friend_list.html', context)

# path converter의 이름이 id
def delete_friend(request,id):
    # print(id)   
    # delete함수는 이미 있는걸 씀 
    # friend 객체들 중에 파라미터로 넘어온 id와 일치하는 id를 가진 객체를 삭제한다
    Friend.objects.get(id = id).delete()

    # 호출할 때 앞에 아무것도 안붙히면 : 현재 디레고리에서 이동
    # 상위 디렉토리 : ../
    # 하위 디렉토리 : ./
    # return HttpResponseRedirect('../../show_all') 이거랑 같음
    return HttpResponseRedirect('/friend/show_all')

def update_friend(request,id):
    friend = Friend.objects.get(id = id)

    # 전송 방식에 따른 화면 표시
    if request.method == "GET":
    #id로 찾은 친구 정보를 템플릿에 표시하기 위해서 
        context = {'friend' : friend}
        return render(request,'friend/friend_update.html', context)
    else:
        # id로 찾은 객체에 대해서 폼의 값으로 원래 객체의 값 덮어쓰기
        friend.friend_name = request.POST['friend_name']
        friend.friend_age = request.POST['friend_age']
        friend.friend_bigo = request.POST['friend_bigo']
            
        friend.save()
        return HttpResponseRedirect('/friend/show_all')
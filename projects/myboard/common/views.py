from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm ,UserChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
# 우리가 만든 custom 회원가입 form,customchangeform
from .forms import UserForm,CustomChangeForm

# Create your views here.
def index(request):
    return render(request,"common/index.html")

def signup(request):
    if request.method =="POST":
        # 요청 객체가 담고 있는 정보로 사용자 생성 폼 만든다
        print(request.POST)
        form = UserCreationForm(request.POST)
        
        if form.is_valid(): # form의 내용이 유효하다면(비어있지 않은지, pw1,2가 동일한지 이메일 형식을 따르는지)
            form.save() #db에 form정보 저장
            
            # 폼에 입력한 값 가져오기
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')

            # 사용자 인증
            user = authenticate(username=username, password=raw_password)
            # 로그인
            login(request,user)

            return redirect('/')
    else:
        print(request.GET)
        form = UserCreationForm(request.GET)
    return render(request,"common/signup.html",{'form':form})

def signup_custom(request):
    if request.method =="POST":
        print(request.POST) #QueryDict 한번 보기

        form = UserForm(request.POST) # request.POST에 담겨있는 정보를 UserForm형식으로 변환
        # form이 유효한가?(is_valid())
        if form.is_valid():
            form.save() # 폼의 내용을 DB(auth user)에 바로 저장

            # 폼의 정보를 취득
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            # 폼에있는 정보를 가져와서 인증을 시킴
            user = authenticate(username = username, password = raw_password, first_name=first_name,last_name=last_name)
            login(request, user) #사용자 인증 후 로그인 

            return redirect('/') # 로그인 하고 메인 페이지로 넘김
    else: # 요청이 get일때 
        form = UserForm() # 비어있는 새폼 만들어주기

    return render(request,'common/signup.html',{'form':form})


def delete(request):
    if request.user.is_authenticated:
        request.user.delete() # user 정보 삭제
        # render나 redirect의 파라미터로 app_name:url_name 작성 가능
        return redirect('common:index')
    
def update(request):
    if request.method =="POST":
        print("POST방식")
        form = CustomChangeForm(request.POST, instance = request.user)
        print("form>>",form)
        if form.is_valid():
            form.save() #form이 유효하다면 해당 내용 저장
            return redirect('common:index')
    else:
        print("get방식")
        form = CustomChangeForm()   
        # customchangeform(instance) 보내면 django가 보내는 form을 사용할 수 있
    return render(request,'common/update.html',{'form':form})

def update(request):
    if request.method =="POST":
        # print("POST방식")
        form = CustomChangeForm(request.POST, instance = request.user)
        # print("form>>",form)
        if form.is_valid():
            form.save() #form이 유효하다면 해당 내용 저장
            return redirect('common:index')
    else:
        # print("get방식")
        form = CustomChangeForm()   
        # customchangeform(instance) 보내면 django가 보내는 form을 사용할 수 있
    return render(request,'common/update.html',{'form':form})

def mypage(request):
    form = CustomChangeForm()
    return render(request,'common/mypage.html',{'form':form})
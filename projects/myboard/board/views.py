from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.core.paginator import Paginator
from django.core import serializers
from django.contrib.auth.decorators import login_required

from json import loads
from .models import Board ,Reply

# Create your views here.

def index(request):
    
    result = None # 필터링 된 리스트
    context = {}
    if 'searchType' in request.GET and 'searchWord' in request.GET:
        search_type = request.GET['searchType'] # get안의 문자열은
        search_word = request.GET['searchWord'] # html의 name속성과 일치해야함
        print("searchType :{}, search_word : {}".format(search_type,search_word))

        #match:java의 switch와 비슷함
        match search_type:
            case 'title': # 검색 기준이 제목일때
                result = Board.objects.filter(title__contains = search_word)
            case 'writer': # 검색 기준이 제목일때
                result = Board.objects.filter(writer__contains = search_word)
            case 'content': # 검색 기준이 제목일때
                result = Board.objects.filter(content__contains = search_word)
        # 검색을 했을 때만 검색 기준과 키워드를 context에 넣는다
        context['searchType'] = search_type
        context['searchWord'] = search_word
    else: # QueryDict에 검색 조건과 키워드가 없을 때
        result = Board.objects.all()
    result = result.order_by("-id")
    paginator = Paginator(result,10)
    page_obj = paginator.get_page(request.GET.get('page'))
    context['page_obj'] = page_obj
    return render(request,'board/index.html', context)

def read(request,id):
    print("read실행")
    # board = Board.objects.all()
    board = Board.objects.get(id = id)

    board.view_count += 1
    board.save()
    context ={
        'board':board #애하고 fk걸려있는 쿼리 셋이 같이 딸려감
        # ',replyList':reply_list
    }
    return render(request,'board/read.html', context)
    # return render(request,'board/board.html', context)

def home(request):
    # 목록으로
    return HttpResponseRedirect("/board/")

# 내가 따로 만든 로그인 url이 있다면 login_url 키워드 변수를 지정해야한다.
@login_required(login_url='common:login')
def write(request):
    if request.method =='GET': #요청방식이 get 방식이면 화면 표시
        return render(request,'board/board_form.html')
    else: # 요청방식이 POST일때 할일
        # 폼의 데이터를 DB에 저장
        title = request.POST['title']
        # writer = request.POST['writer'] #??
        content = request.POST['content']
        author = request.user
        Board.objects.create(
            title = title,
            author = author, # user객체 저장
            content = content
        )
        print(request.user)
        return HttpResponseRedirect('/board/')


@login_required(login_url='common:login')
def update(request,id):
    board = Board.objects.get(id=id)
    # 전송 방식에 따른 화면 표시
    if board.author.username == request.user.username:
        return
    if request.method == "GET":
    #id로 찾은 친구 정보를 템플릿에 표시하기 위해서
        context = {'board' : board}
        return render(request,'Board/board_update.html', context)
    else:
        # id로 찾은 객체에 대해서 폼의 값으로 원래 객체의 값 덮어쓰기
        board.title = request.POST['title']
        board.content = request.POST['content']

        board.save()
        #수정 후에 해당 글로 다시 이동
    redirect_url = '/board/' +str(id) +'/'
    return HttpResponseRedirect(redirect_url)

@login_required(login_url='common:login')
def delete(request,id):
    print("id :",id)
    # 해당 객체를 가져옴
    board = Board.objects.get(id=id)

    # 글 작성자의 id와 접속한 사람의 id가 같을때
    if board.author.username == request.user.username:
        board.delete()
    return HttpResponseRedirect('/board/')

#댓글 쓰기
def write_reply(request):
    id = request.POST['id']
    rt = request.POST["reply_content"]
    user = request.user
    print(user)
    board = Board.objects.get(id=id) 
    board.reply_set.create(
        user = user,
        reply_content = rt
    )
    return JsonResponse("",safe=False)

def load_reply(request):
    id = request.POST['id']
    print(id)
    # 해당하는 board id 에 달려있는 모든 reply 가져오기
    # 1번 방법
    # reply.objects.filter(board=id)
    # 2번 방법
    reply_list = Board.objects.get(id=id).reply_set.all()

    # QuerySet 그 자체는 JS에서는 알 수 없는 타입
    # 그래서 JSON타입으로 형변환
    serialized_list = serializers.serialize("json",reply_list)
    # response = {'response':serialized_list}
    response = {'response':serialized_list}
    return JsonResponse(response)

def delete_reply(request):
    id = request.POST['id']
    rid = request.POST['rid']
    Board.objects.get(id=id).reply_set.get(id=rid).delete()
    return JsonResponse("",safe=False) #딕셔너리 형식으로 보내줘야함

def update_reply(request):
    id = request.POST['id']
    rid = request.POST['rid']
    reply = Board.objects.get(id=id).reply_set.get(id=rid)
    reply.reply_content = request.POST['rt']
    reply.save()
    return JsonResponse("",safe=False)

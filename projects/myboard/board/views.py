from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse,FileResponse
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
        print(request.POST)
        print(request.FILES)
        # 폼의 데이터를 DB에 저장
        title = request.POST['title']
        # writer = request.POST['writer'] #??
        content = request.POST['content']
        author = request.user # 요청에 들어있는 user객체

        board =  Board(
            title = title,
            author = author, # user객체 저장
            content = content
        )
        # get메소드 사용하는 ㅣ융
        # 딕셔너리에서 존재하지 않는 키를 딕셔너리 [킬]
        # 딕셔너리.get("키") ->None
        if request.FILES.get("uploadFile"):
            upload_file = request.FILES['uploadFile']
            # 요청에 들어있던 첨부파일을 모델에 설정
            board.attached_file = upload_file
            board.original_file_name = upload_file.name
        board.save()
        return HttpResponseRedirect('/board/')


# 글 수정
@login_required(login_url='common:login')
def update(request, id):
    board = Board.objects.get(id = id)

    # 로그인 정보가 맞지 않을 때
    if board.author.username != request.user.username:
        return HttpResponseRedirect('/board/')

    if request.method == 'GET':
        context = {'board' : board }
        return render(request , 'board/board_update.html', context)
    else:
        board.title = request.POST['title']
        # board.writer = request.POST['writer']
        board.content = request.POST['content']

        #첨부 파일이 있다면
        if request.FILES.get("uploadFile"):
            upload_file = request.FILES["uploadFile"]
            #요청에 들어있던 첨부파일을 모델에 설정
            board.attached_file = upload_file
            board.original_file_name = upload_file.name
        else: #첨부파일이 없다면
            board.attached_file=None
            board.original_file_name=None
        board.save() # save를 해야 DB에 반영됨!!!

        # 수정 후에 해당 글로 다시 이동
        redirect_url  = '/board/' + str(id) + '/'
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


def write_reply(request,id):
    print(request.POST)

    user = request.user # 어떻게
    print("user:",user)
    reply =  loads(request.body) #요청의 body를 해석
    print("reply:",reply)

    reply_text = reply['replyText']
    board = Board.objects.get(id = id)
    board.reply_set.create(
        reply_content = reply_text,
        user = user
    )
    return JsonResponse({'result':'success'})

def load_reply(request,id):
    reply_list  = Board.objects.get(id = id).reply_set.all()
    reply_dict_list = []

    #reply_list의 정보를 가지고 dictionary 만들기
    for reply in reply_list:
        reply_dict = {
            'id' : reply.id,
            'username' : reply.user.username,
            'replyText':reply.reply_content,
            'inputDate' :reply.input_date
        }
        reply_dict_list.append(reply_dict)
    context = {'replyList':reply_dict_list}
    return JsonResponse(context)

def update_reply(request,id):
    if request.method =='GET':
        board = Board.objects.get(id=id)
        rid = request.GET['rid']
        replyText = board.reply_set.get(id=rid) #reply_set.get다시 공부할 것
        context ={
            #rid에 해당하는 reply 객체의 id하고 replyText
            'rid':rid,
            'replyText':replyText.reply_content
        }
        print(type(context))
        return JsonResponse(context)
    else:
        print("post로 받았음")

        request_body = loads(request.body)
        rid = request_body['rid']
        reply_text = request_body['replyText']
        reply = Board.objects.get(id=id).reply_set.get(id=rid)
        reply.reply_content = reply_text
        reply.save()
        return JsonResponse("",safe=False)

def delete_reply(request,id):
    request_board = loads(request.body)
    rid = request_board['rid']
    Board.objects.get(id=id).reply_set.get(id=rid).delete()
    return JsonResponse("",safe=False) #딕셔너리 형식으로 보내줘야함

def download(request,id):
    print(id)
    board = Board.objects.get(id=id)
    attached_file = board.attached_file
    original_file_name = board.original_file_name

    # 글 번호에 달려있던 첨부파일로 파일형식 응답 객체 생성
    response = FileResponse(attached_file)
    response['Content-Disposition'] = 'attachment; filename =%s'%original_file_name # 이 응답은 이런 컨텐츠 입니다.

    return response
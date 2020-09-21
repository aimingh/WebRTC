from django.shortcuts import render
from django.http import HttpResponse

# 홈태그 이용해서 데이터 전송할 때 {% crsf_token %} crsf 토큰이 필요
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
import base64
#====================================================================
import time, os, json
from board.models import WebRTC 
from django.db import connection
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from common.forms import UserForm
from django.contrib.auth.decorators import login_required
#====================================================================
@login_required(login_url='common:login')
def index(request):
    return render(request, "index.html")

@csrf_exempt
def save(request):
    if (request.method == 'POST'):
        # id = request.POST.get('id')
        # pwd = request.POST.get('pwd')
        img = request.POST.get('img')
        img = img.replace('data:image/png;base64,', '')
        img = img.replace(' ', '+')
        d = base64.b64decode(img)   # 디코딩

        # 폴더 생성
        # now_path = make_folder()
        file = open('test1.png', mode="wb")
        file.write(d)
        file.close()
        # 폴더 만들고  /upload/2020/09/14/20200914_1234.png
        # 드론식별값, 이미지path, 이미지명, 저장된시간분초, 상대방 ip
        # gps 좌표값, 브라우저에서 좌표 알수 있다. (클라이언트)
        # 주소 (클라이언트로부터 받아오자)도 저장
        # 리스트, 상세보기 화면 - 삭제 기능

        # print(img)
        # print(id)
        # print(pwd)
    return HttpResponse("receive")

# ======================================================================================================================
# ======================================================================================================================
def home(request):
    return render(request, 'home.html')
# ======================================================================================================================
# ======================================================================================================================
# 쿼리 기반 db 저장
def dbsave_q(name, path, groupid, x, y, address, droneid):
    cursor =  connection.cursor()
    sql = f'''
    insert into board_webrtc(name, path, groupid, x, y, address, droneid) values('{name}', '{path}', '{groupid}', '{x}', '{y}', '{address}', '{droneid}');
    '''
    cursor.execute(sql)

# 시간 기준으로 폴더와 파일 이름 생성, 경로와 파일 이름을 반환
def make_folder_name(groupname):
    now = time.localtime()
    rootpath = f"/{now.tm_year}/{now.tm_mon}/{now.tm_mday}/"
    folder_name = groupname
    path = rootpath + folder_name
    filename = f"{now.tm_hour}_{now.tm_min}_{now.tm_sec}.png"
    try:
        if not os.path.exists('.' + path):
            os.makedirs('.' + path)
            print('.' + path)
        return path, filename
    except Exception:
        print('making folder error')

# 이미지 파일 저장
def save_png(img, groupname):
    now_path, filename = make_folder_name(groupname) # 시간기반 폴더 파일 이름 생성
    file = open('.' + now_path + '/' + filename, mode="wb")
    file.write(img)
    file.close()
    return  now_path, filename

# base64 디코딩
def decode_base64(img):
    img = img.replace('data:image/png;base64,', '')
    img = img.replace(' ', '+')
    d = base64.b64decode(img)  
    return d

# ajax로 받은 데이터를 기반으로 데이터베이스에 데이터를 저장, 영상을 서버에 저장
@csrf_exempt
def start(request):
    if (request.method == 'POST'):
        # ajax에서 정보를 받는다.
        groupname = request.POST.get('groupname')
        dronename = request.POST.get('dronename')
        img = request.POST.get('img')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        address = request.POST.get('address[documents][0][address][address_name]')
        
        d = decode_base64 (img) # base64 이미지 디코딩, 디코딩된 이미지를 반환
        if address != None:
            now_path, filename = save_png(d, groupname)    # 이미지를 저장하고 파일 이름과 경로를 반환
            dbsave_q(filename, now_path, groupname, longitude, latitude, address, dronename)
        return HttpResponse("receive")

# ======================================================================================================================
# 로그인 관리
# ======================================================================================================================
# 등록
def signup(request):
    """
    계정생성
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})

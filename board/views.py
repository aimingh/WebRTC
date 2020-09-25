from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
from django.utils import timezone

# 추가 라이브러리
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from common.CommonPage import CommonPage
import os, shutil
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

#==================================================================================================
#==================================================================================================
# 커서로 받은 내용을 dict로 전환
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

# 페이징 처리를 위해 페이지네이터 사용
def paging(request, datalist, num=10):
    page = request.GET.get('page', '1')
    paginator = Paginator(datalist, num)
    page_obj = paginator.get_page(page)
    page = int(page)
    maxpage = num*((page-1)//num)+10
    minpage = num*((page-1)//num)+1
    return page_obj, (maxpage), (minpage)

# http://127.0.0.1/board/grouplist 
# 그룹에 리스트     
@login_required(login_url='common:login')
def group(request):
    cursor =  connection.cursor()
    # 그룹마다 처음 행을 가져오는 쿼리
    sql = f'''
    select * from board_webrtc where id in (SELECT min(id) FROM board_webrtc GROUP BY groupid);
    '''
    cursor.execute(sql)
    WebRTC_list = dictfetchall(cursor)
    # 페이징 처리 페이지네이터 이용
    page_obj, maxpage, minpage = paging(request, WebRTC_list)
    context = {'question_list': page_obj, 'maxpage':maxpage, 'minpage':minpage}
    return render(request, 'board/webrtc_group.html', context)

# http://127.0.0.1/board/grouplist/1 
# gourpid 처음과 마지막 파일을 미리보기하고, 포함된 파일 리스트를 보여준다.
@login_required(login_url='common:login')
def groupid(request, groupid):
    cursor =  connection.cursor()
    # 특정 그룹의 처음과 마지막 데이터를 가져오는 쿼리
    sql = f'''
    SELECT * FROM board_webrtc WHERE id = (SELECT min(id) FROM board_webrtc WHERE groupid = '{groupid}')
    UNION
    SELECT * FROM board_webrtc WHERE id = (SELECT max(id) FROM board_webrtc WHERE groupid = '{groupid}');
    '''
    cursor.execute(sql)
    WebRTC_list = dictfetchall(cursor)

    sql = f'''
    SELECT * FROM board_webrtc WHERE groupid = '{groupid}';
    '''
    cursor.execute(sql)
    group_list = dictfetchall(cursor)
    page_obj, maxpage, minpage = paging(request, group_list)
    context = {'list':WebRTC_list, 'question_list':page_obj, 'maxpage':maxpage, 'minpage':minpage}
    return render(request, 'board/webrtc_groupview.html', context)

# http://127.0.0.1/board/detaillist/1 
# id를 이용하여 하나의 데이터 전체 정보 열람
@login_required(login_url='common:login')
def detailid(request, id):
    cursor =  connection.cursor()
    sql = f'''
    SELECT * FROM board_webrtc WHERE id ='{id}';
    '''
    print(sql)
    cursor.execute(sql)
    l = dictfetchall(cursor)
    print(l)
    return render(request, 'board/webrtc_list.html', {'l': l[0] } )

# 데이터베이스에서 그룹을 지우고 지운 그룹의 경로 반환
def deleteGroupID(groupid):
    cursor =  connection.cursor()
    sql = f'''
    SELECT path FROM board_webrtc WHERE groupid in ({groupid}) GROUP BY groupid;
    DELETE FROM board_webrtc WHERE groupid in ({groupid});
    '''
    print(sql)
    cursor.execute(sql)
    return [row for row in cursor.fetchall()]

# 그룹삭제
@csrf_exempt
def deleteGroup(request):
    if (request.method == 'POST'):
        checkListID = request.POST.get('checkListID')
        groupids = checkListID[:-1].split(',')
        s = '"' + '","'.join(groupids) + '"'
        path = deleteGroupID(s)
        for i in range(len(path)):
            if os.path.exists('.' + path[i][0]):
                shutil.rmtree('.' + path[i][0])
    return redirect('board:grouplist')

# 데이터베이스에서 id 데이터를 지우고 지운 데이터의 경로 반환
def deleteid(id):
    cursor =  connection.cursor()
    # 특정 그룹의 처음과 마지막 데이터를 가져오는 쿼리
    sql = f'''
    SELECT path, name FROM board_webrtc WHERE id in ({id});
    DELETE FROM board_webrtc WHERE id in ({id});
    '''
    cursor.execute(sql)
    return ['.' + row[0] + '/'+ row[1] for row in cursor.fetchall()]
def search_groupid(id):
    cursor =  connection.cursor()
    # 특정 그룹의 처음과 마지막 데이터를 가져오는 쿼리
    sql = f'''
    SELECT groupid FROM board_webrtc WHERE id in ({id});
    '''
    cursor.execute(sql)
    return [row  for row in cursor.fetchall()]

# 아이디 삭제
@csrf_exempt
def deleteID(request):
    if (request.method == 'POST'):
        checkListID = request.POST.get('checkListID')
        id = checkListID[:-1].split(',')
        groupid = search_groupid(id[0])
        s = '"' + '","'.join(id) + '"'
        paths = deleteid(s)
        for path in paths:
            if os.path.exists(path):
                os.remove(path)
    return redirect('board:groupdetail', groupid=groupid[0][0])


#==================================================================================================
#==================================================================================================

from django.contrib import admin
from django.urls import path, include
from . import views

app_name='board' #이렇게 써줘야 없어진다  

urlpatterns = [
    # 추가된 url
    path('grouplist', views.group, name="grouplist"),#http://127.0.0.1/board/grouplist 
    path('grouplist/<str:groupid>', views.groupid, name="groupdetail"),#http://127.0.0.1/board/grouplist/1 
    path('detaillist/<int:id>', views.detailid, name="detail"),#http://127.0.0.1/board/detaillist/1 
    path('deleteGroup', views.deleteGroup, name="deleteGroup"), #http://127.0.0.1/board/deleteGroup 
    path('deleteID', views.deleteID, name="deleteID"), #http://127.0.0.1/board/deleteID 
]

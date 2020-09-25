from django.db import models

# id 파일이름 파일패스 그룹id x y 주소 드론일련번호
class WebRTC(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    path = models.CharField(max_length=200)
    groupid = models.CharField(max_length=200)
    x = models.FloatField()
    y = models.FloatField()  
    address = models.TextField() 
    droneid = models.CharField(max_length=200)
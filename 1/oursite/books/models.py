from django.db import models

# Create your models here.
class User(models.Model):
    UserName=models.CharField(max_length=50)
    PassWord=models.CharField(max_length=30)
    Level=models.CharField(max_length=30)
class Things(models.Model):
    Level=models.CharField(max_length=30)
    Name=models.CharField(max_length=50)
    FID=models.CharField(max_length=20)
    Xing=models.CharField(max_length=30)
    BDate=models.CharField(max_length=30)
    S=models.CharField(max_length=30)
    
    
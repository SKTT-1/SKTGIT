# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class User(models.Model):
    Level = models.CharField(max_length = 5)
    Acount = models.CharField(max_length = 20, primary_key=True)
    Password = models.CharField(max_length = 20)
    Name = models.CharField(max_length = 20)
    Belong = models.CharField(max_length = 20)
    
    def __unicode__(self):
        return self.Name
        
class Form(models.Model):
    Formnumber = models.AutoField(primary_key=True)
    Level = models.CharField(max_length = 5)
    Action = models.CharField(max_length = 10)
    Applicant = models.CharField(max_length = 20)
    Amount = models.CharField(max_length = 10)
    Date = models.DateField()
    Reason = models.TextField(max_length = 200)
    State = models.CharField(max_length = 10)
    Suggestion = models.TextField(max_length = 200)
    
    def __str__(self):
        return str(self.Formnumber)

class AddForm(models.Model):
    Formnumber = models.AutoField(primary_key=True)
    Applicant = models.CharField(max_length = 20)
    Level = models.CharField(max_length = 5)
    Kind = models.CharField(max_length = 10)
    Name = models.CharField(max_length = 10)
    Date = models.DateField()
    Formatx = models.CharField(max_length = 20)
    Price = models.CharField(max_length = 20)
    Amount = models.CharField(max_length = 10)
    Reason = models.TextField(max_length = 200)
    State = models.CharField(max_length = 10)
    Suggestion = models.TextField(max_length = 200,null=True)
    
    def __str__(self):
        return str(self.Formnumber)

class Device(models.Model):
    SN = models.AutoField(primary_key=True)
    Level = models.CharField(max_length = 5)
    Kind = models.CharField(max_length = 10)
    Name = models.CharField(max_length = 10)
    Date = models.DateField()
    Formatx = models.CharField(max_length = 20)
    Price = models.CharField(max_length = 20)
    State = models.CharField(max_length = 10)
    Borrower = models.CharField(max_length = 20)
    Form = models.IntegerField(null = True,default = 0)
    def __str__(self):
        return str(self.SN)


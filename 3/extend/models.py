# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class Belong(models.Model):
    Name = models.CharField(max_length = 20)
    Address = models.CharField(max_length = 20)
    Phone = models.CharField(max_length = 20)
    Email = models.CharField(max_length = 20)
    
    def __unicode__(self):
        return self.Name
    
class User(models.Model):
    Level = models.CharField(max_length = 5)
    Acount = models.CharField(max_length = 20, primary_key=True)
    Password = models.CharField(max_length = 20)
    Name = models.CharField(max_length = 20)
    Belong = models.ForeignKey(Belong, db_column = 'Belong')
    Email = models.CharField(max_length = 20)
    Phone = models.CharField(max_length = 20)
    
    def __unicode__(self):
        return self.Name

class Form(models.Model):
    Formnumber = models.AutoField(primary_key=True)
    Level = models.CharField(max_length = 5)
    Action = models.CharField(max_length = 10)
    Applicant = models.CharField(max_length = 20)
    Amount = models.CharField(max_length = 10)
    Date = models.DateField()
    Time = models.CharField(max_length = 20, null = True, blank = True)
    ToBelong = models.CharField(max_length = 20, null = True, blank = True)
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
    SN = models.CharField(max_length = 20, primary_key=True)
    Level = models.CharField(max_length = 5)
    Kind = models.CharField(max_length = 10)
    Name = models.CharField(max_length = 10)
    Date = models.DateField()
    Formatx = models.CharField(max_length = 20)
    Price = models.CharField(max_length = 20)
    State = models.CharField(max_length = 10)
    Borrower = models.CharField(max_length = 20)
    Form = models.IntegerField(null = True,default = 0)
    User = models.ForeignKey(User, db_column = 'user', null = True, blank = True)
    def __str__(self):
        return str(self.SN)


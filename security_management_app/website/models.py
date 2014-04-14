from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Vulnerability(models.Model):
    cve = models.CharField(max_length=30,unique=True)
    summary = models.CharField(max_length=1000)
    def __unicode__(self):
        return self.cve 

class Application(models.Model):
    cpe = models.CharField(max_length=200,unique=True)
    vulnerability = models.ManyToManyField(Vulnerability)

    def __unicode__(self):
        return self.name

class Device(models.Model):
    owner = models.ForeignKey(User)
    uid = models.CharField(max_length=50,unique=True)
    os = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50) #User can add a memorable name to a device?
    
    nickname.blank = True

    def __unicode__(self):
        if self.nickname is not None:
            return self.nickname + " (" + self.uid + ")"
        else:
            return self.uid



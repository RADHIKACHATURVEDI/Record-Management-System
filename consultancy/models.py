from django.db import models

# Create your models here.
class Data(models.Model):
    name = models.CharField(max_length=100)
    username=models.CharField(max_length=100)
    date_of_birth = models.CharField(max_length=15,default="10/6/2001")
    email = models.CharField(max_length=100)
    investigation = models.CharField(max_length=1000)
    history = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
from django.db import models
from django.utils import timezone
# Create your models here.
class RealEstateObject(models.Model):
    idCrawlerJob =  models.CharField(null=True, max_length=100)

    codePost = models.IntegerField(null=True)
    typePost = models.CharField(null=True, max_length=255)

    title = models.TextField(null=True)
    price = models.BigIntegerField(null=True)
    area = models.DecimalField(null=True, max_digits=19, decimal_places=5)

    type = models.TextField(null=True)
    date = models.DateTimeField(default=timezone.now)
    address = models.TextField(null=True)
    numberBedrooms = models.IntegerField(null=True)
    numberToilets = models.IntegerField(null=True)
    sizeFront = models.DecimalField(null=True, max_digits=19, decimal_places=5)
    numberFloor = models.IntegerField(null=True)
    wardin = models.DecimalField(null=True, max_digits=19, decimal_places=5)
    homeDirection = models.CharField(null=True, max_length=255)
    balconyDirection = models.CharField(null=True, max_length=255)
    interior = models.TextField(null=True)
    longitude = models.DecimalField(null=True, max_digits=19, decimal_places=5)
    latitude = models.DecimalField(null=True, max_digits=19, decimal_places=5)
    
    nameOwner = models.CharField(null=True, max_length=255)
    mobile = models.CharField(null=True, max_length=100)
    email = models.CharField(null=True, max_length=100)
    link = models.TextField(null=True)
    projectName = models.CharField(null=True, max_length=255)
    projectSize = models.TextField(null=True)
    projectOwner = models.CharField(null=True, max_length=255)
    startDatePost = models.DateTimeField(default=timezone.now)
    endDatePost = models.DateTimeField(default=timezone.now)

class Employee(models.Model):
    title = models.CharField(max_length=255)
    price = models.IntegerField(default=0)
    content = models.CharField(max_length=255)
class Quote(models.Model):
    unique_id = models.CharField(max_length=100, null=True)
    text = models.TextField()
    author = models.CharField(max_length=512)
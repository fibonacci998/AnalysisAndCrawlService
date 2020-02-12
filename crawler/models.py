from django.db import models
from django.utils import timezone
# Create your models here.
class RealEstateObject(models.Model):
    idCrawlerJob =  models.CharField(max_length=100, null=True)

    idPost = models.IntegerField()
    typePost = models.CharField(max_length=255)

    title = models.CharField(max_length=255)
    price = models.BigIntegerField(null=True)
    area = models.DecimalField(max_digits=19, decimal_places=5)

    date = models.DateTimeField(default=timezone.now)
    # title = models.CharField(max_length=255)
    # price = models.IntegerField(default=0)
    # content = models.CharField(max_length=255)

class Employee(models.Model):
    title = models.CharField(max_length=255)
    price = models.IntegerField(default=0)
    content = models.CharField(max_length=255)
class Quote(models.Model):
    unique_id = models.CharField(max_length=100, null=True)
    text = models.TextField()
    author = models.CharField(max_length=512)
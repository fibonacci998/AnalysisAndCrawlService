from django.db import models
from django.utils import timezone
# Create your models here.
class RealEstateObject(models.Model):
    idCrawlerJob =  models.IntegerField()

    idPost = models.IntegerField()
    typePost = models.CharField(max_length=255)

    title = models.CharField(max_length=255)
    price = models.BigIntegerField()
    area = models.DecimalField(max_digits=19, decimal_places=5)

    date = models.DateTimeField(default=timezone.now)
    # title = models.CharField(max_length=255)
    # price = models.IntegerField(default=0)
    # content = models.CharField(max_length=255)

class Employee(models.Model):
    title = models.CharField(max_length=255)
    price = models.IntegerField(default=0)
    content = models.CharField(max_length=255)
from django.db import models

# Create your models here.
class RealEstateObject(models.Model):
    idCrawlerJob =  models.IntegerField(default=None)

    idPost = models.IntegerField(default=None)
    typePost = models.CharField(max_length=255, default=None)

    title = models.CharField(max_length=255, default=None)
    price = models.BigIntegerField(default=None)
    area = models.DecimalField(max_digits=19, decimal_places=5)



from django.contrib import admin
from .models import RealEstateObject, Employee, Quote
# Register your models here.

admin.site.register(RealEstateObject)
admin.site.register(Employee)
admin.site.register(Quote)
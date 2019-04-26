from django.contrib import admin
from app01 import models
# Register your models here.


admin.site.register(models.Author)
admin.site.register(models.Publisher)
admin.site.register(models.Book)
from django.db import models
from django.utils import timezone
# Create your models here.
class Item(models.Model):
    item_name =models.CharField(max_length=100)
    item_count=models.IntegerField(null=False,default=1)

class Order(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    orderdate = models.DateTimeField(default = timezone.now)
    quantity = models.IntegerField(null=False)
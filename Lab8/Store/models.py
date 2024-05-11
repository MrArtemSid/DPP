from django.db import models
from django.utils import timezone


class Storage(models.Model):
    id_storage = models.AutoField(primary_key=True)
    city = models.CharField(max_length=50)
    region = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.city} {self.region} (id={self.id_storage})'


class Item(models.Model):
    id_item = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    cnt = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name} (id={self.id_item})'


class Seller(models.Model):
    id_seller = models.AutoField(primary_key=True)
    id_storage = models.ForeignKey(Storage, on_delete=models.CASCADE, to_field='id_storage')
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50)
    age = models.IntegerField()
    position = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.second_name} {self.first_name} (id={self.id_seller})'


class SellerPlan(models.Model):
    id_seller = models.OneToOneField(Seller, on_delete=models.CASCADE, primary_key=True, to_field='id_seller')
    plan_date = models.DateField(default=timezone.now)
    sells_plan = models.IntegerField()
    actual_sells_plan = models.IntegerField()

    def __str__(self):
        return f'{self.id_seller} {self.plan_date}'


class StoragePlan(models.Model):
    id_storage = models.OneToOneField(Storage, on_delete=models.CASCADE, primary_key=True, to_field='id_storage')
    plan_date = models.DateField(default=timezone.now)
    sells_plan = models.IntegerField()
    actual_sells_plan = models.IntegerField()

    def __str__(self):
        return f'{self.id_storage} {self.plan_date}'


class Sells(models.Model):
    id_sell = models.AutoField(primary_key=True)
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, to_field='id_storage')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, to_field='id_item')
    cnt = models.IntegerField()
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, to_field='id_seller')
    sell_data = models.DateField(default=timezone.now)

    def __str__(self):
        return f'{self.id_sell} {self.sell_data}'

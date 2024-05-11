from django.contrib import admin

from Store.models import Storage, StoragePlan, Sells, Item, SellerPlan, Seller

admin.site.register(Storage)
admin.site.register(StoragePlan)
admin.site.register(Sells)
admin.site.register(Item)
admin.site.register(SellerPlan)
admin.site.register(Seller)
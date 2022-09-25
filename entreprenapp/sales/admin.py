from django.contrib import admin
from .models import Saler,Customer, Item, Invoice, OrderLine, Estimate

admin.site.register(Saler)
admin.site.register(Customer)
admin.site.register(Item)
admin.site.register(OrderLine)
admin.site.register(Estimate)
admin.site.register(Invoice)

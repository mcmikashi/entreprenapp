from django.contrib import admin

from .models import Customer, Estimate, Invoice, Item, OrderLine, Saler

admin.site.register(Saler)
admin.site.register(Customer)
admin.site.register(Item)
admin.site.register(OrderLine)
admin.site.register(Estimate)
admin.site.register(Invoice)

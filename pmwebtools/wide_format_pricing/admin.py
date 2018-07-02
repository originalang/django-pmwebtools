from django.contrib import admin
from .models import print_price, base_price, profit_markup, non_profit_markup, paper_type

admin.site.register(print_price)
admin.site.register(base_price)
admin.site.register(profit_markup)
admin.site.register(non_profit_markup)
admin.site.register(paper_type)

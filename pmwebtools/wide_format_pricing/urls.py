from django.urls import path, re_path
from . import views

app_name = 'wide_format_pricing'

urlpatterns = [
    path('calculator/', views.wf_calculator, name='calculator'),
    path('calculate-price/', views.calculate_price, name='calculate-price'),
    path('price-display/', views.price_display.as_view(), name='price-display'),
    path('base-price-display/', views.base_price_display.as_view(), name='base-price-display'),
    path('non-profit-markup-display/', views.non_profit_markup_display.as_view(), name='non-profit-markup-display'),
    path('profit-markup-display/', views.profit_markup_display.as_view(), name='profit-markup-display'),
    re_path(r'change-default/(?P<object>[\w\-]+)/(?P<pk>[0-9]+)/(?P<rev>[\w\-]+)/$', views.make_default, name='change-default'),
]

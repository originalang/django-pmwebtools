from django.shortcuts import render
from .models import base_price, print_price, non_profit_markup, profit_markup, paper_type
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.contrib.auth.decorators import login_required

@login_required(login_url='pam:login')
def wf_calculator(request):
    paper_types_list = paper_type.objects.all()
    return render(request, 'wide_format_pricing/wide_format_price_calculator.html', {'paper_types_list':paper_types_list})


class price_display(generic.ListView):
    template_name = 'wide_format_pricing/price_display.html'

    def get_queryset(self):
        return print_price.objects.all()


class base_price_display(generic.ListView):
    template_name = 'wide_format_pricing/base_price_display.html'

    def get_queryset(self):
        return base_price.objects.all()


class non_profit_markup_display(generic.ListView):
    template_name = 'wide_format_pricing/non_profit_markup_display.html'

    def get_queryset(self):
        return non_profit_markup.objects.all()


class profit_markup_display(generic.ListView):
    template_name = 'wide_format_pricing/profit_markup_display.html'

    def get_queryset(self):
        return profit_markup.objects.all()


def make_default(request, pk, object, rev):
    model_names = {'print_price':print_price, 'base_price':base_price, 'non_profit_markup':non_profit_markup, 'profit_markup':profit_markup}

    model_param = model_names[object]
    new_default = model_param.objects.get(pk=pk)

    new_default.is_default = True
    new_default.save()

    return HttpResponseRedirect(reverse('wide_format_pricing:' + rev))


def calculate_price(request):
    base_price_default = base_price.objects.get(is_default=True)
    non_profit_markup_default = non_profit_markup.objects.get(is_default=True)
    profit_markup_default = profit_markup.objects.get(is_default=True)

    form = request.POST
    quantity = int(form['quantity'])
    paper_selection = form['paper-type']
    height = int(form['height'])
    width = int(form['width'])

    if form['measure'] == 'Inches':
        square_inches = height * width
        paper = paper_type.objects.get(name=paper_selection)
        default_paper_cost = paper.print_price_set.get(is_default=True)

        if default_paper_cost.cost_context == 'per Square Foot':
            cost = default_paper_cost.cost / 12
        else:
            cost = default_paper_cost.cost

        if form['customer-classification'] == 'Internal':
            final_price = (quantity * (cost * square_inches)) + base_price_default.base_price
            return HttpResponse(final_price)
        elif form['customer-classification'] == 'Non-Profit':
            price = ((quantity * (cost * square_inches)) + base_price_default.base_price)
            final_price = price + (price * (non_profit_markup_default.markup_percent/100))
            return HttpResponse(final_price)
        elif form['customer-classification'] == 'Profit':
            price = ((quantity * (cost * square_inches)) + base_price_default.base_price)
            final_price = price + (price * (profit_markup_default.markup_percent/100))
            return HttpResponse(final_price)
    if form['measure'] == 'Feet':
        square_feet = height * width
        paper = paper_type.objects.get(name=paper_selection)
        default_paper_cost = paper.print_price_set.get(is_default=True)

        if default_paper_cost.cost_context == 'per Square Inch':
            cost = default_paper_cost.cost * 12
        else:
            cost = default_paper_cost.cost

        if form['customer-classification'] == 'Internal':
            final_price = (quantity * (cost * square_inches)) + base_price_default.base_price
            return HttpResponse(final_price)
        elif form['customer-classification'] == 'Non-Profit':
            price = ((quantity * (cost * square_inches)) + base_price_default.base_price)
            final_price = price + (price * (non_profit_markup_default.markup_percent/100))
            return HttpResponse(final_price)
        elif form['customer-classification'] == 'Profit':
            price = ((quantity * (cost * square_inches)) + base_price_default.base_price)
            final_price = price + (price * (profit_markup_default.markup_percent/100))
            return HttpResponse(final_price)

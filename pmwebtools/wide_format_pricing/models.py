from django.db import models

cost_context_choices = (
                    ('per Square Inch', 'per Square Inch'),
                    ('per Square Foot', 'per Square Foot')
                )


class paper_type(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class print_price(models.Model):
    paper_type = models.ForeignKey(paper_type, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    cost = models.DecimalField(max_digits=7, decimal_places=5)
    cost_context = models.CharField(max_length=50, choices=cost_context_choices, default='per Square Inch')
    is_default = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_default:
            all_price_true = type(self).objects.filter(is_default=True, paper_type=self.paper_type)
            all_price_true.exclude()
            all_price_true.update(is_default=False)

        super(print_price, self).save(*args, **kwargs)


class base_price(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    base_price = models.DecimalField(max_digits=3, decimal_places=2)
    is_default = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_default:
            all_base_prices = type(self).objects.filter(is_default=True)
            all_base_prices.exclude(pk=self.pk)
            all_base_prices.update(is_default=False)

        super(base_price, self).save(*args, **kwargs)


class non_profit_markup(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    markup_percent = models.DecimalField(max_digits=5, decimal_places=2)    # as percentage
    is_default = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_default:
            all_default_markup = type(self).objects.filter(is_default=True)
            all_default_markup.exclude(pk=self.pk)
            all_default_markup.update(is_default=False)

        super(non_profit_markup, self).save(*args, **kwargs)


class profit_markup(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    markup_percent = models.DecimalField(max_digits=5, decimal_places=2)    # as percentage
    is_default = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_default:
            all_default_markup = type(self).objects.filter(is_default=True)
            all_default_markup.exclude(pk=self.pk)
            all_default_markup.update(is_default=False)

        super(profit_markup, self).save(*args, **kwargs)

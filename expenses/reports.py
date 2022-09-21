from collections import OrderedDict

from django.db.models import Sum, Value, Count
from django.db.models.functions import Coalesce, TruncMonth, TruncYear

from expenses.models import Expense


def summary_per_category(queryset):
    return OrderedDict(sorted(
        queryset
        .annotate(category_name=Coalesce('category__name', Value('-')))
        .order_by()
        .values('category_name')
        .annotate(s=Sum('amount'))
        .values_list('category_name', 's'),
    ))


def total_amount_spent(queryset):
    result = OrderedDict(queryset.aggregate(Sum('amount')))
    return result

# Групировка  по числам в месяце

def total_summary_per_number_month(queryset):
    return OrderedDict(sorted(
        queryset
        .annotate(data=Coalesce('date', Value('-')))
        .order_by()
        .values('date')
        .annotate(s=Sum('amount'))
        .values_list('date', 's'),
    ))


def total_summary_per_year_month(queryset):
    return OrderedDict(sorted(
        queryset
        .annotate(month=TruncMonth('date'), year=TruncYear('date'))
        .values('month', 'year')
        .annotate(summa_all=Sum('amount'))
        .values_list('month', 'summa_all'),
    ))




def get_about_categories(queryset):
    about_categories = queryset \
        .annotate(count_category=Count('expense')) \
        .order_by('-count_category')
    return about_categories



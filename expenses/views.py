from django.views.generic.list import ListView

from .forms import ExpenseSearchForm
from .models import Expense, Category
from .reports import summary_per_category, total_amount_spent, total_summary_per_year_month, \
    total_summary_per_number_month, get_about_categories


class ExpenseListView(ListView):
    model = Expense
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list
        # all tabl


        form = ExpenseSearchForm(self.request.GET)

        if form.is_valid():

            name = form.cleaned_data.get('name', '').strip()
            date = form.cleaned_data.get('date', '')
            # category = form.cleaned_data.get('category')
            categories = form.cleaned_data.get('categories') # добавили строку
            #cleaned_data.get('categories =проверенные данные из формы поля категория
            sort_by = form.cleaned_data.get('sort_by')


            if name:
                queryset = queryset.filter(name__icontains=name)

            if date:
                #queryset = queryset.filter(name__icontains=date)
                queryset = queryset.filter(date=date)

            if categories:
                category_list = []
                for i in categories: # пишем несколько категорий в форме и добавляем их в список
                    category_list.append(i)
                queryset = queryset.filter(category__name__in=category_list)
                # в таблице в колонке категории берет те данные где категория равна значению из списка cat_list

            if sort_by:
                queryset = queryset.order_by(sort_by)




        return super().get_context_data(
            form=form,
            object_list=queryset,
            summary_per_category=summary_per_category(queryset),
            total_amount_spent=total_amount_spent(queryset),
            total_summary_per_year_month=total_summary_per_year_month(queryset),
            total_summary_per_number_month=total_summary_per_number_month(queryset),

            **kwargs)

class CategoryListView(ListView):
    model = Category
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list
        context = super().get_context_data(
            object_list=queryset,
            about_categories=get_about_categories(queryset),
            **kwargs)
        return context



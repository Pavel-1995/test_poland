from django import forms
from django.db.models import Count

from .models import Expense, Category




class ExpenseSearchForm(forms.ModelForm):
    date = forms.DateField(input_formats=['%m-%d-%Y'])# ++
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.annotate(total=Count('expense')).filter(total__gt=0), widget=forms.CheckboxSelectMultiple)
    # ModelMultipleChoiceField- выбор из колонки нескольких строчек ,,, потом формируем запрос что с ними будем делать
    sort_by = forms.ChoiceField(label='sort', required=False, choices=[
        ['category', 'category'],
        ['date', 'date_increasing'],
        ['-date', 'date_descending']
                                         ])
    class Meta:
        model = Expense
        #fields = ('name',)
        fields = ('name', 'date', 'categories', 'sort_by')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['date'].required = False  # ++ str поля не обязательное
        self.fields['categories'].required = False




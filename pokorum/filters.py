from django_filters import FilterSet, DateFilter, CharFilter
from django.forms import DateInput
from .models import Comments, Post


class CommentFilter(FilterSet):
    '''
    Фильтрация отзывов по критериям
    - позже какой-либо даты;
    - по содержанию отзыва;
    - всё вместе.
    '''
    published_date = DateFilter(field_name='published_date',
                                lookup_expr='gt',
                                label='Опубликовано после даты:',
                                widget=DateInput(format='%d.%m.%Y', attrs={'type': 'date'})
                                )

    comment = CharFilter(field_name='comment', lookup_expr='icontains', label='Содержание отзыва:')

    class Meta:
        model = Comments
        fields = ['published_date']

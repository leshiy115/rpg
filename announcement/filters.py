from django_filters import FilterSet, DateFilter
from .models import Comment
from django.forms import SelectDateWidget



class CommentFilter(FilterSet):

    time_created = DateFilter(label='Дата после',
        lookup_expr='gt',
        widget=SelectDateWidget(years=[2023, 2024]))

    class Meta:
        model = Comment
        fields = ['anons']






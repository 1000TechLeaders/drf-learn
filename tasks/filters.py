from django_filters import rest_framework as filters

from .models import Task


class TaskFilter(filters.FilterSet):
    # date expression - month, day, week, date, time
    category = filters.CharFilter(field_name='category__name', lookup_expr='icontains')
    name = filters.CharFilter(field_name='name', lookup_expr='iexact')
    added_at = filters.NumberFilter(field_name='created_at__date', lookup_expr='day')
    # level = filters.NumberFilter(field_name='level', lookup_expr='lte')
    custom_level = filters.NumberFilter(method='get_custom_level')
    ordering = filters.CharFilter(method='get_ordering')

    class Meta:
        model = Task
        fields = ('completed', 'category', 'added_at', 'expired_at', 'ordering')

    def get_custom_level(self, queryset, name, value):
        return queryset.filter(completed=False, level__gt=value)


    def get_ordering(self, queryset, name, value):
        value_name = {
            'publicated_at': 'created_at',
            '-publicated_at': '-created_at',
        }
        print(name, value, 'okkk')
        return queryset.order_by(value_name.get(value))

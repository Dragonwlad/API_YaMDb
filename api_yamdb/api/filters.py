import django_filters

from reviews.models import Title


class TitleFilter(django_filters.FilterSet):
    """
    Фильтр для запросов к объектам модели Title.
    Фильтрация осуществляется по slug категории,
    slug жанра, году и/или названию.
    """
    category = django_filters.CharFilter(
        field_name='category__slug', lookup_expr='iexact'
    )
    genre = django_filters.CharFilter(
        field_name='genre__slug', lookup_expr='iexact'
    )
    year = django_filters.NumberFilter(
        field_name='year', lookup_expr='exact'
    )
    name = django_filters.CharFilter(
        field_name='name', lookup_expr='iexact'
    )

    class Meta:
        model = Title
        fields = ('category', 'genre', 'year', 'name')

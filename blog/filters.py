import django_filters

from .models import Post

class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Post
        fields = '__all__'
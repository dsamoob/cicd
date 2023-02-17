from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from logistic.models import Product, Stock
from rest_framework.response import Response
from logistic.serializers import ProductSerializer, StockSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['title', 'description', ]
    search_fields = ['title', 'description', ]
    pagination_class = LimitOffsetPagination
    # при необходимости добавьте параметры фильтрации

    @action(['GET'], detail=False)
    def test(self, request):
        return Response('HELLO')


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['products']
    search_fields = ['products__title', 'products__description']
    pagination_class = LimitOffsetPagination

    # при необходимости добавьте параметры фильтрации

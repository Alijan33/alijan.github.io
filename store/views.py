from django.shortcuts import get_object_or_404
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import RetrieveModelMixin, DestroyModelMixin
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet,  ReadOnlyModelViewSet, GenericViewSet
from rest_framework import status
from .models import *
from .seriializers import *
from .fillters import *
from .pagination import *


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = {'title', 'description'}
    ordering_fields = ['unit_price', 'last_update']

    def get_queryset(self):
        queryset = Product.objects.all()
        collection_id = self.request.query_params.get('collection_id')
        if collection_id is not None:
            queryset.filter(collection_id=collection_id)

        return queryset

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, * args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response(status=status.HTTP_204_NO_CONTENT)

        return super().destroy(request, *args, **kwargs)


class CollectionViewSet(ReadOnlyModelViewSet):
    queryset = Collection.objects.annotate(
        product_count=Count('product')).all()
    serializer_class = CollectionSerializer

    def delete(self, request, pk):
        collection = get_object_or_404(Collection.objects.annotate(
            product_count=Count('product')), pk=pk)
        if collection.product.count() > 0:
            return Response({'error': 'Collection can not be deleted'})
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return{'product_id': self.kwargs['product_ok']}


class CartViewset(CreateModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    serializer_class = CartItemSerializer
    http_method_names = 'get', 'post', 'patch', 'delete'


    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif  self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects \
            .filter(cart_id=self.kwargs['cart_pk']) \
            .select_related('product')

from django.contrib import admin, messages
from django.db.models import Count, fields
from django.utils.html import format_html
from urllib.parse import urlencode
from . models import *
from tags.models import TaggedItem
from django.urls import reverse
from django.db.models.query import QuerySet
# Register your models here.


admin.site.register(Adress)
admin.site.register(Promotion)
admin.site.register(Cart)
admin.site.register(CartItem)


class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low')
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)


class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    prepopulated_field = {
        'sulg': ['title']
    }
    actions = ['clear_inventory']
    list_display = ['title', 'unit_price',
                    'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_filter = ['collection', 'last_update', InventoryFilter]
    list_per_page = 10
    list_select_related = ['collection']
    search_fields = ['title']

    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Law'
        return 'OK'

    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        update_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{update_count} product were successfully updated',
            messages.ERROR
        )


admin.site.register(Product, ProductAdmin)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['frist_name', 'last_name', 'membership', ]
    list_editable = ['membership']
    list_per_page = 10
    list_select_related = ['user']
    ordering = ['user__frist_name', 'user__last_name', ]
    search_fields = 'frist_name__istartswith', 'last_name__istart'


@admin.display(ordering='orders_count')
def orders(self, customer):
    url = (
        reverse('admin:store_order_changelist')
        + '?'
    )


admin.site.register(Customer, CustomerAdmin)


class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    min_num = 1
    max_num = 10
    extra = 0


admin.site.register(OrderItem)


class OrderAdmin(admin.ModelAdmin):
    # autocomplete_fields = ['customer']
    list_display = ['id', 'placed_at', ]


admin.site.register(Order, OrderAdmin)


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (reverse('admin:store_product_changelist') + '?' +
               urlencode({'collection__id': str(collection.id)}))
        return format_html(
            '<a herf="{}">{}</a>', url, collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count('product'))

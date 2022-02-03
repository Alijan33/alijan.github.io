from store.models import Product
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.contenttypes.admin import GenericTabularInline
from store.admin import ProductAdmin
from tags.models import TaggedItem
from . models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email')
        }),
    )


class TagInline(GenericTabularInline):
    autocomplete_field = ['tag']
    models = TaggedItem


# class CustomProductAdmin(ProductAdmin):
#     inlines = [TagInline]


admin.site.unregister(Product)
admin.site.register(Product,)

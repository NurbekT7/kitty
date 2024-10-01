from django.contrib import admin
from django.utils.html import mark_safe
from django.conf import settings

from django.contrib.auth.models import Group
admin.site.unregister(Group)

from apps.cats.models import Breeds, Cats, CatRating


@admin.register(Breeds)
class BreedsAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "get_img",)
    list_display_links = list_display

    def get_img(self, obj):
        if obj.img:
            return mark_safe(f'<img style="border-radius: 50%;" src="{obj.img.url}" width="50" height="50" />')
        return "No image"

    get_img.short_description = 'Изображение'


@admin.register(Cats)
class CatsAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "color", "age", "img",)
    list_display_links = list_display

    def get_img(self, obj):
        if obj.img:
            return mark_safe(f'<img style="border-radius: 50%;" src="{obj.img.url}" width="50" height="50" />')
        return "No image"

    get_img.short_description = 'Изображение'


admin.site.register(CatRating)
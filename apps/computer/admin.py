from django.contrib import admin
from .models import Category, Laptop, LaptopImage


class TabularInlineImage(admin.TabularInline):
    model = LaptopImage
    extra = 0
    fields = ['image']


class LaptopAdmin(admin.ModelAdmin):
    model = Laptop
    inlines = [TabularInlineImage, ]


admin.site.register(Laptop, LaptopAdmin)
admin.site.register(Category)
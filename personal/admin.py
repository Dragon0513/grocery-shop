from django.contrib import admin

from personal.models import Category, Food, Section

# Register your models here.
admin.site.register(Category)
admin.site.register(Section)
admin.site.register(Food)

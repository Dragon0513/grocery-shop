from django.contrib import admin

from personal.models import (
    Category,
    Food,
    Note,
    Section,
    ShoppingList,
    ShoppingListItem,
)

# Register your models here.
admin.site.register(Category)
admin.site.register(Section)
admin.site.register(Food)
admin.site.register(ShoppingList)
admin.site.register(ShoppingListItem)
admin.site.register(Note)

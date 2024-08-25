from django.urls import path

from personal.views import (
    AllShoppingListView,
    CategoryView,
    CreateShoppingListItemView,
    CreateShoppingListView,
    DeleteShoppingListItemView,
    DeleteShoppingListView,
    SelectShoppingListView,
    ShareShoppingListView,
    ShoppingListView,
    UpdateShoppingListItemView,
    UpdateShoppingListView,
)

urlpatterns = [
    path("category/<int:pk>", CategoryView.as_view(), name="category"),
    path("lists/", AllShoppingListView.as_view(), name="lists"),
    path("lists/create", CreateShoppingListView.as_view(), name="list_create"),
    path("lists/<int:pk>", ShoppingListView.as_view(), name="list"),
    path("lists/<int:pk>/update", UpdateShoppingListView.as_view(), name="list_update"),
    path("lists/<int:pk>/delete", DeleteShoppingListView.as_view(), name="list_delete"),
    path("lists/<int:pk>/share", ShareShoppingListView.as_view(), name="list_share"),
    path("food/<int:pk>/lists", SelectShoppingListView.as_view(), name="select_lists"),
    path(
        "food/<int:food_pk>/lists/<int:list_pk>/item/create",
        CreateShoppingListItemView.as_view(),
        name="item_create",
    ),
    path(
        "items/<int:pk>/update",
        UpdateShoppingListItemView.as_view(),
        name="item_update",
    ),
    path(
        "items/<int:pk>/delete",
        DeleteShoppingListItemView.as_view(),
        name="item_delete",
    ),
]

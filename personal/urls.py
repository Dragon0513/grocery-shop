from django.urls import path

from personal.views import (
    AllNotesView,
    AllShoppingListView,
    AllTasksView,
    CategoryView,
    CreateNoteView,
    CreateShoppingListItemView,
    CreateShoppingListView,
    CreateTaskView,
    DeleteNoteView,
    DeleteShoppingListItemView,
    DeleteShoppingListView,
    DeleteTaskView,
    SelectShoppingListView,
    ShareShoppingListView,
    ShoppingListView,
    UpdateNoteView,
    UpdateShoppingListItemView,
    UpdateShoppingListView,
    UpdateTaskView,
)
from system.views import CategoriesView

urlpatterns = [
    path("categories/", CategoriesView.as_view(), name="categories"),
    path("categories/<int:pk>", CategoryView.as_view(), name="category"),
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
    path("tasks", AllTasksView.as_view(), name="tasks"),
    path("tasks/create", CreateTaskView.as_view(), name="task_create"),
    path("tasks/<int:pk>/update", UpdateTaskView.as_view(), name="task_update"),
    path("tasks/<int:pk>/delete", DeleteTaskView.as_view(), name="task_delete"),
    path("notes", AllNotesView.as_view(), name="notes"),
    path("notes/create", CreateNoteView.as_view(), name="note_create"),
    path("notes/<int:pk>/update", UpdateNoteView.as_view(), name="note_update"),
    path("notes/<int:pk>/delete", DeleteNoteView.as_view(), name="note_delete"),
]

from django.urls import path

from personal.views import CategoryView

urlpatterns = [
    path("category/<int:pk>", CategoryView.as_view(), name="category"),
]

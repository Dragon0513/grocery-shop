from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views import generic

from personal.models import Category, Food, Section
from system.mixins import LegalRequirementMixin


# Create your views here.
class CategoryView(LoginRequiredMixin, LegalRequirementMixin, generic.DetailView):
    model = Category
    template_name = "pages/category.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get("search", "")

        if search_query:
            # Filter foods based on the search query
            foods = Food.objects.filter(
                section__category=self.object, name__icontains=search_query
            )
        else:
            # Get all foods for the category
            foods = Food.objects.filter(section__category=self.object)

        # Get sections that have the filtered foods
        sections = Section.objects.filter(
            Q(category=self.object) & Q(food__in=foods)
        ).distinct()

        context["sections"] = sections
        context["foods"] = foods

        return context

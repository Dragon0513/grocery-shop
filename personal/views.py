from django.contrib.auth.mixins import LoginRequiredMixin
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

        context["sections"] = Section.objects.filter(category=self.object)

        if search_query:
            context["foods"] = Food.objects.filter(
                section__category=self.object, name__icontains=search_query
            )
        else:
            context["foods"] = Food.objects.filter(section__category=self.object)

        return context

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext as _
from django.views import generic

from personal.models import (
    Category,
    Food,
    Note,
    Section,
    ShoppingList,
    ShoppingListItem,
    Task,
)
from system.mixins import LegalRequirementMixin

User = get_user_model()


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
            foods = Food.objects.filter(section__category=self.object)

        sections = Section.objects.filter(
            Q(category=self.object) & Q(food__in=foods)
        ).distinct()

        context["sections"] = sections
        context["foods"] = foods

        return context


class AllShoppingListView(LoginRequiredMixin, LegalRequirementMixin, generic.ListView):
    model = ShoppingList
    template_name = "pages/shopping_list.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["created_lists"] = ShoppingList.objects.filter(owner=self.request.user)
        context["shared_lists"] = ShoppingList.objects.filter(
            shared_with=self.request.user
        )

        return context


class CreateShoppingListView(
    LoginRequiredMixin, LegalRequirementMixin, generic.CreateView
):
    model = ShoppingList
    fields = ["name"]
    template_name = "pages/create/shopping_list.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Einkaufsliste")
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("home")


class ShoppingListView(LoginRequiredMixin, LegalRequirementMixin, generic.UpdateView):
    model = ShoppingList
    template_name = "pages/detail/shopping_list.html"
    login_url = reverse_lazy("login")
    fields = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shopping_list = self.get_object()
        items = shopping_list.shoppinglistitem_set.all()

        context["shopping_list"] = shopping_list
        context["items"] = items
        context["share"] = shopping_list.owner == self.request.user
        return context

    def post(self, request, *args, **kwargs):
        shopping_list = self.get_object()
        items = shopping_list.shoppinglistitem_set.all()

        for item in items:
            checkbox_value = request.POST.get(f"item_{item.pk}", "off")
            item.status = True if checkbox_value == "on" else False
            item.save()

        return redirect(reverse("list", kwargs={"pk": shopping_list.pk}))

    def dispatch(self, request, *args, **kwargs):
        shopping_list = self.get_object()
        if (
            shopping_list.owner != request.user
            and request.user not in shopping_list.shared_with.all()
        ):
            return redirect(reverse("home"))
        return super().dispatch(request, *args, **kwargs)


class UpdateShoppingListView(
    LoginRequiredMixin, LegalRequirementMixin, generic.UpdateView
):
    model = ShoppingList
    fields = ["name"]
    template_name = "pages/create/shopping_list.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        shopping_list = self.get_object()

        context["title"] = _("Einkaufsliste")
        context["operation"] = "update"
        context["list"] = shopping_list
        return context

    def dispatch(self, request, *args, **kwargs):
        shopping_list = self.get_object()
        if shopping_list.owner != request.user:
            return redirect(reverse("home"))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("list", kwargs={"pk": self.object.pk})


class DeleteShoppingListView(LoginRequiredMixin, generic.DeleteView):
    model = ShoppingList
    template_name = "pages/root/account_delete.html"
    success_url = reverse_lazy("lists")
    login_url = reverse_lazy("login")

    def dispatch(self, request, *args, **kwargs):
        shopping_list = self.get_object()
        if shopping_list.owner != request.user:
            return redirect(reverse("home"))
        return super().dispatch(request, *args, **kwargs)


class ShareShoppingListView(
    LoginRequiredMixin, LegalRequirementMixin, generic.DetailView
):
    model = ShoppingList
    template_name = "pages/share_shopping_list.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shopping_list = self.get_object()
        users = User.objects.exclude(id=self.request.user.id)

        context["users"] = users
        context["shared_users"] = shopping_list.shared_with.all()
        return context

    def post(self, request, *args, **kwargs):
        shopping_list = self.get_object()
        selected_user_ids = request.POST.getlist("shared_users")

        shared_users = User.objects.filter(id__in=selected_user_ids)
        shopping_list.shared_with.set(shared_users)

        return redirect("list", pk=shopping_list.pk)

    def dispatch(self, request, *args, **kwargs):
        shopping_list = self.get_object()
        if shopping_list.owner != request.user:
            return redirect(reverse("home"))
        return super().dispatch(request, *args, **kwargs)


class SelectShoppingListView(
    LoginRequiredMixin, LegalRequirementMixin, generic.ListView
):
    model = ShoppingList
    template_name = "pages/select_shopping_list.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        food_pk = self.kwargs.get("pk")

        context["food_pk"] = food_pk
        context["created_lists"] = ShoppingList.objects.filter(owner=self.request.user)
        context["shared_lists"] = ShoppingList.objects.filter(
            shared_with=self.request.user
        )

        return context


class CreateShoppingListItemView(
    LoginRequiredMixin, LegalRequirementMixin, generic.CreateView
):
    model = ShoppingListItem
    fields = ["quantity", "unit_per_item", "unit"]
    template_name = "pages/create/shopping_list_item.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Einkaufsware")
        shopping_list = get_object_or_404(ShoppingList, pk=self.kwargs["list_pk"])
        food = get_object_or_404(Food, pk=self.kwargs["food_pk"])
        context["shopping_list"] = shopping_list
        context["food"] = food
        return context

    def get_initial(self):
        initial = super().get_initial()
        shopping_list = get_object_or_404(ShoppingList, pk=self.kwargs["list_pk"])
        initial["shopping_list"] = shopping_list
        return initial

    def form_valid(self, form):
        shopping_list = get_object_or_404(ShoppingList, pk=self.kwargs["list_pk"])
        food = get_object_or_404(Food, pk=self.kwargs["food_pk"])
        form.instance.shopping_list = shopping_list
        form.instance.food = food
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("list", kwargs={"pk": self.object.shopping_list.pk})


class UpdateShoppingListItemView(
    LoginRequiredMixin, LegalRequirementMixin, generic.UpdateView
):
    model = ShoppingListItem
    fields = ["quantity", "unit_per_item", "unit"]
    template_name = "pages/create/shopping_list_item.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        item = self.get_object()

        context["title"] = _("Einkaufsware")
        context["item"] = item
        context["operation"] = "update"
        return context

    def get_success_url(self):
        return reverse_lazy("list", kwargs={"pk": self.object.shopping_list.pk})


class DeleteShoppingListItemView(LoginRequiredMixin, generic.DeleteView):
    model = ShoppingListItem
    template_name = "pages/root/account_delete.html"
    login_url = reverse_lazy("login")

    def get_success_url(self):
        return reverse_lazy("list", kwargs={"pk": self.object.shopping_list.pk})


class AllNotesView(LoginRequiredMixin, LegalRequirementMixin, generic.ListView):
    model = Note
    template_name = "pages/notes.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["notes"] = Note.objects.filter(owner=self.request.user)

        return context


class CreateNoteView(LoginRequiredMixin, LegalRequirementMixin, generic.CreateView):
    model = Note
    fields = ["title", "content", "color"]
    template_name = "pages/create/note.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Notiz")
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("notes")


class UpdateNoteView(LoginRequiredMixin, LegalRequirementMixin, generic.UpdateView):
    model = Note
    fields = ["title", "content", "color"]
    template_name = "pages/create/note.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Notiz")
        context["operation"] = "update"
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("notes")


class DeleteNoteView(LoginRequiredMixin, generic.DeleteView):
    model = Note
    template_name = "pages/root/account_delete.html"
    login_url = reverse_lazy("login")

    def get_success_url(self):
        return reverse_lazy("notes")


class AllTasksView(LoginRequiredMixin, LegalRequirementMixin, generic.ListView):
    model = Task
    template_name = "pages/tasks.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = Task.objects.filter(owner=self.request.user)

        context["tasks_to_do"] = tasks.filter(status="not_done")
        context["tasks_in_progress"] = tasks.filter(status="in_progress")
        context["tasks_done"] = tasks.filter(status="done")

        return context


class CreateTaskView(LoginRequiredMixin, LegalRequirementMixin, generic.CreateView):
    model = Task
    fields = ["text", "status"]
    template_name = "pages/create/task.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Aufgabe")
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("tasks")


class UpdateTaskView(LoginRequiredMixin, LegalRequirementMixin, generic.UpdateView):
    model = Task
    fields = ["text", "status"]
    template_name = "pages/create/task.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Aufgabe")
        context["operation"] = "update"
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("tasks")


class DeleteTaskView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    template_name = "pages/root/account_delete.html"
    login_url = reverse_lazy("login")

    def get_success_url(self):
        return reverse_lazy("tasks")

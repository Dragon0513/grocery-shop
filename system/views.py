from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic

from personal.models import Category
from system.forms import LoginForm, SignUpForm
from system.models import LegalUser

from .mixins import LegalRequirementMixin

User = get_user_model()


# Create your views here.
def sign_in(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect("home")
        form = LoginForm()
        return render(request, "pages/authentication/login.html", {"form": form})

    elif request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, "Erfolgreich angemeldet!")
                return redirect("home")

        messages.error(request, "Benutzername oder Passwort ist falsch.")
        return render(request, "pages/authentication/login.html", {"form": form})


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "pages/authentication/signup.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        LegalUser.objects.create(
            user=self.object, privacy=False, disclaimer=False, terms=False
        )
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@login_required
def custom_logout(request):
    logout(request)
    return redirect("home")


class HomeView(LoginRequiredMixin, LegalRequirementMixin, generic.ListView):
    model = User
    template_name = "pages/root/home.html"
    login_url = reverse_lazy("login")


class CategoriesView(
    LoginRequiredMixin,
    LegalRequirementMixin,
    generic.ListView,
):
    model = Category
    template_name = "pages/categories.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class SettingsView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = "pages/root/settings.html"

    login_url = reverse_lazy("login")


class SettingsUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = User
    template_name = "pages/root/settings_update.html"
    fields = ["first_name", "last_name", "username", "email"]

    login_url = reverse_lazy("login")

    def get_success_url(self):
        return reverse_lazy("settings")


class SettingsDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = User
    template_name = "pages/root/settings_delete.html"
    success_url = reverse_lazy("home")

    login_url = reverse_lazy("login")

    def get_object(self):
        if self.request.user.is_authenticated:
            return self.request.user


class ImpressumView(generic.ListView):
    model = User
    template_name = "pages/legal/impressum.html"


class PrivacyView(generic.UpdateView):
    model = LegalUser
    fields = []
    template_name = "pages/legal/privacy.html"
    success_url = reverse_lazy("disclaimer")

    def get_object(self, queryset=None):
        if self.request.user.is_authenticated:
            return self.request.user.legaluser

    def form_valid(self, form):
        form.instance.privacy = True
        form.instance.save()
        return redirect(
            "disclaimer"
            if not form.instance.disclaimer
            else "terms" if not form.instance.terms else "home"
        )


class DisclaimerView(generic.UpdateView):
    model = LegalUser
    fields = []
    template_name = "pages/legal/disclaimer.html"
    success_url = reverse_lazy("home")

    def get_object(self, queryset=None):
        if self.request.user.is_authenticated:
            return self.request.user.legaluser

    def form_valid(self, form):
        form.instance.disclaimer = True
        form.instance.save()
        return redirect(
            "privacy"
            if not form.instance.privacy
            else "terms" if not form.instance.terms else "home"
        )


class TermsView(generic.UpdateView):
    model = LegalUser
    fields = []
    template_name = "pages/legal/terms.html"
    success_url = reverse_lazy("home")

    def get_object(self, queryset=None):
        return self.request.user.legaluser

    def form_valid(self, form):
        form.instance.terms = True
        form.instance.save()
        return redirect("home")

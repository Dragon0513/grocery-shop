from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View, generic

from personal.models import Category
from system.forms import LoginForm, SignUpForm
from system.models import LegalUser, SocialUser

from .mixins import BlockedUserRedirectMixin, LegalRequirementMixin

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
        SocialUser.objects.create(
            user=self.object,
        )
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


class DetailUserView(
    LoginRequiredMixin,
    LegalRequirementMixin,
    BlockedUserRedirectMixin,
    generic.DetailView,
):
    model = User
    template_name = "pages/users/detail.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user_social, created = SocialUser.objects.get_or_create(
            user=self.request.user
        )
        user = self.object
        user_social, created = SocialUser.objects.get_or_create(user=user)

        is_friend = user in current_user_social.friends.all()
        is_friend_request_sent = user in current_user_social.sent_requests.all()
        is_friend_request_received = user in current_user_social.received_requests.all()
        is_blocked = user in current_user_social.blocked.all()

        context["friends"] = user_social.friends.count()
        context["is_friend"] = is_friend
        context["is_friend_request_sent"] = is_friend_request_sent
        context["is_friend_request_received"] = is_friend_request_received
        context["is_blocked"] = is_blocked
        return context


class DetailUserFriendsView(
    LoginRequiredMixin,
    LegalRequirementMixin,
    BlockedUserRedirectMixin,
    generic.DetailView,
):
    model = User
    template_name = "pages/users/friends.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user_social, created = SocialUser.objects.get_or_create(
            user=self.request.user
        )
        user = self.object
        user_social, created = SocialUser.objects.get_or_create(user=user)

        friends_users = user_social.friends.values_list("id", flat=True)
        friends = User.objects.filter(pk__in=friends_users)

        friends_with_status = []
        for friend in friends:
            friend_social, _ = SocialUser.objects.get_or_create(user=friend)
            is_friend = friend in current_user_social.friends.all()
            is_blocked = friend in current_user_social.blocked.all()

            friends_with_status.append(
                {"user": friend, "is_friend": is_friend, "is_blocked": is_blocked}
            )

        context["friends_with_status"] = friends_with_status
        context["is_friend"] = user in current_user_social.friends.all()
        context["is_friend_request_sent"] = (
            user in current_user_social.sent_requests.all()
        )
        context["is_friend_request_received"] = (
            user in current_user_social.received_requests.all()
        )
        context["is_blocked"] = user in current_user_social.blocked.all()
        return context


class BlockUserView(LoginRequiredMixin, View):
    def post(self, request, pk):
        user_to_block = get_object_or_404(User, pk=pk)
        if user_to_block != request.user:
            current_user_social, created = SocialUser.objects.get_or_create(
                user=request.user
            )
            user_to_block_social, created = SocialUser.objects.get_or_create(
                user=user_to_block
            )

            current_user_social.blocked.add(user_to_block)

            if user_to_block in current_user_social.friends.all():
                current_user_social.friends.remove(user_to_block)
                user_to_block_social.friends.remove(request.user)

            if user_to_block in current_user_social.received_requests.all():
                current_user_social.received_requests.remove(user_to_block)
                user_to_block_social.sent_requests.remove(request.user)
            if user_to_block in current_user_social.sent_requests.all():
                current_user_social.sent_requests.remove(user_to_block)
                user_to_block_social.received_requests.remove(request.user)

        return redirect(reverse("profile_detail", kwargs={"pk": pk}))


# views.py
class UnblockUserView(LoginRequiredMixin, View):
    def post(self, request, pk):
        user_to_unblock = get_object_or_404(User, pk=pk)
        current_user_social = SocialUser.objects.get(user=request.user)

        if user_to_unblock in current_user_social.blocked.all():
            current_user_social.blocked.remove(user_to_unblock)

        return redirect(reverse("profile_detail", kwargs={"pk": pk}))


class SendFriendRequestView(LoginRequiredMixin, View):
    def post(self, request, pk):
        user_to_request = get_object_or_404(User, pk=pk)
        if user_to_request != request.user:
            current_user_social, created = SocialUser.objects.get_or_create(
                user=request.user
            )
            user_to_request_social, created = SocialUser.objects.get_or_create(
                user=user_to_request
            )
            if user_to_request not in current_user_social.sent_requests.all():
                current_user_social.sent_requests.add(user_to_request)
                user_to_request_social.received_requests.add(request.user)
        return redirect(reverse("profile_detail", kwargs={"pk": pk}))


class CancelFriendRequestView(LoginRequiredMixin, View):
    def post(self, request, pk):
        user_to_cancel = get_object_or_404(User, pk=pk)
        if user_to_cancel != request.user:
            current_user_social, created = SocialUser.objects.get_or_create(
                user=request.user
            )
            user_to_cancel_social, created = SocialUser.objects.get_or_create(
                user=user_to_cancel
            )
            if user_to_cancel in current_user_social.sent_requests.all():
                current_user_social.sent_requests.remove(user_to_cancel)
                user_to_cancel_social.received_requests.remove(request.user)
        return redirect(reverse("profile_detail", kwargs={"pk": pk}))


class RemoveFriendView(LoginRequiredMixin, View):
    def post(self, request, pk):
        user_to_remove = get_object_or_404(User, pk=pk)
        if user_to_remove != request.user:
            current_user_social, created = SocialUser.objects.get_or_create(
                user=request.user
            )
            user_to_remove_social, created = SocialUser.objects.get_or_create(
                user=user_to_remove
            )

            if user_to_remove in current_user_social.friends.all():
                current_user_social.friends.remove(user_to_remove)
                user_to_remove_social.friends.remove(request.user)

        return redirect(reverse("profile_detail", kwargs={"pk": pk}))


class SearchView(LoginRequiredMixin, LegalRequirementMixin, generic.ListView):
    model = User
    template_name = "pages/root/search.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = User.objects.exclude(id=self.request.user.id)

        current_user_social = SocialUser.objects.get(user=self.request.user)
        friends = current_user_social.friends.all()
        blocked_users = current_user_social.blocked.all()
        users_with_friendship_and_block = []

        for user in users:
            user_social = SocialUser.objects.get(user=user)
            if self.request.user not in user_social.blocked.all():
                users_with_friendship_and_block.append(
                    {
                        "user": user,
                        "is_friend": user in friends,
                        "is_blocked": user in blocked_users,
                    }
                )

        context["users_list"] = users_with_friendship_and_block
        return context


class NotificationsView(LoginRequiredMixin, LegalRequirementMixin, generic.ListView):
    model = User
    template_name = "pages/root/notifications.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        social_user = SocialUser.objects.get(user=self.request.user)
        context["notifications"] = social_user.received_requests.all()
        return context


class AcceptFriendRequestView(LoginRequiredMixin, View):
    def post(self, request, pk):
        user_to_accept = get_object_or_404(User, pk=pk)
        social_user = SocialUser.objects.get(user=request.user)
        user_to_accept_social = SocialUser.objects.get(user=user_to_accept)

        if user_to_accept in social_user.received_requests.all():
            social_user.friends.add(user_to_accept)
            social_user.received_requests.remove(user_to_accept)
            user_to_accept_social.friends.add(request.user)
            user_to_accept_social.sent_requests.remove(request.user)

        return redirect(reverse("notifications"))


class DeclineFriendRequestView(LoginRequiredMixin, View):
    def post(self, request, pk):
        user_to_decline = get_object_or_404(User, pk=pk)
        social_user = SocialUser.objects.get(user=request.user)

        if user_to_decline in social_user.received_requests.all():
            social_user.received_requests.remove(user_to_decline)
            user_to_decline_social = SocialUser.objects.get(user=user_to_decline)
            user_to_decline_social.sent_requests.remove(request.user)

        return redirect(reverse("notifications"))


class AccountView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = "pages/root/account.html"

    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        social_user = SocialUser.objects.get(user=self.request.user)

        context["friends"] = social_user.friends.count()

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
        if self.request.user.is_authenticated:
            return self.request.user.legaluser

    def form_valid(self, form):
        form.instance.terms = True
        form.instance.save()
        return redirect("home")

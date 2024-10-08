from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _

User = get_user_model()


class SocialUser(models.Model):
    friends = models.ManyToManyField(
        User,
        related_name="friends_with",
        blank=True,
        verbose_name=_("Freunde"),
    )
    sent_requests = models.ManyToManyField(
        User,
        related_name="sent_friend_requests",
        blank=True,
        verbose_name=_("Gesendete Anfragen"),
    )
    received_requests = models.ManyToManyField(
        User,
        related_name="received_friend_requests",
        blank=True,
        verbose_name=_("Erhaltene Anfragen"),
    )
    blocked = models.ManyToManyField(
        User,
        related_name="blocked",
        blank=True,
        verbose_name=_("Blockiert"),
    )
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name=_("Benutzer")
    )


class LegalUser(models.Model):
    privacy = models.BooleanField(verbose_name=_("Datenschutzerklärung"), default=False)
    disclaimer = models.BooleanField(
        verbose_name=_("Haftungsausschluss"), default=False
    )
    terms = models.BooleanField(verbose_name=_("Nutzungsrichtlinien"), default=False)

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name=_("Benutzer")
    )

    def __str__(self):
        return _("Legal User: {username}").format(username=self.user.username)


class Role(models.Model):
    ROLE_CHOICES = [
        ("Admin", "Admin"),
        ("Moderator", "Moderator"),
        ("Premium", "Premium"),
        ("Verifiziert", "Verifiziert"),
        ("Standard", "Standard"),
    ]

    name = models.CharField(
        max_length=50, choices=ROLE_CHOICES, verbose_name=_("Rolle")
    )
    priority = models.IntegerField(verbose_name=_("Stufe"))

    def __str__(self):
        return f"Role: {self.name}, Stufe: {self.priority}"


class ConfigUser(models.Model):
    role = models.ForeignKey(
        Role, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Rolle")
    )
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name=_("Benutzer")
    )

    def __str__(self):
        return f"{self.user}, {self.role}"

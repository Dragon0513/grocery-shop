from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _

User = get_user_model()


# Create your models here.
class Category(models.Model):
    name = models.CharField(verbose_name=_("Kategorie"), max_length=20)
    icon = models.CharField(verbose_name=_("Icon"), max_length=15)

    def __str__(self):
        return self.name


class Section(models.Model):
    name = models.CharField(verbose_name=_("Sektion"), max_length=50)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name=_("Kategorie")
    )

    def __str__(self):
        return str(self.category) + " - " + self.name


class Food(models.Model):
    name = models.CharField(verbose_name=_("Nahrung"), max_length=50)
    section = models.ForeignKey(
        Section, on_delete=models.CASCADE, verbose_name=_("Sektion")
    )

    def __str__(self):
        return str(self.section) + " - " + self.name


class ShoppingList(models.Model):
    name = models.CharField(verbose_name=_("Einkaufsliste"), max_length=50)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_("Benutzer")
    )
    shared_with = models.ManyToManyField(
        User, related_name="shared_lists", blank=True, verbose_name=_("Geteilt mit")
    )

    def __str__(self):
        return self.name


class ShoppingListItem(models.Model):
    UNIT_CHOICES = [
        ("kg", "Kilogram"),
        ("g", "Gram"),
        ("mg", "Milligram"),
        ("l", "Liter"),
    ]

    shopping_list = models.ForeignKey(
        ShoppingList, on_delete=models.CASCADE, verbose_name=_("Einkaufsliste")
    )
    food = models.ForeignKey(Food, on_delete=models.CASCADE, verbose_name=_("Nahrung"))
    quantity = models.IntegerField(verbose_name=_("Menge"), default=1)
    unit = models.CharField(
        verbose_name=_("Einheit"),
        max_length=2,
        choices=UNIT_CHOICES,
        default="kg",
    )
    unit_per_item = models.DecimalField(
        verbose_name=_("Einheit pro Stück"), max_digits=10, decimal_places=2, default=1
    )
    status = models.CharField(
        verbose_name=_("Status"),
        max_length=20,
        choices=[
            ("not_done", _("Nicht erledigt")),
            ("in_progress", _("In Bearbeitung")),
            ("done", _("Erledigt")),
        ],
        default="not_done",
    )

    def __str__(self):
        return f"{self.food.name} ({self.quantity} {self.get_unit_display()}) in {self.shopping_list.name}"


class Note(models.Model):
    COLORS = [
        ("gray", _("Grau")),
        ("red", _("Rot")),
        ("orange", _("Orange")),
        ("yellow", _("Gelb")),
        ("green", _("Grün")),
        ("cyan", _("Türkis")),
        ("blue", _("Blau")),
        ("purple", _("Violett")),
    ]
    title = models.CharField(verbose_name=_("Titel"), max_length=10)
    content = models.TextField(verbose_name=_("Inhalte"), max_length=200)
    color = models.CharField(
        verbose_name=_("Farben"),
        max_length=10,
        choices=COLORS,
        default="gray",
    )
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_("Benutzer")
    )

    def __str__(self):
        return f"{self.title} - Owner: {self.owner}"


class Task(models.Model):
    STATUS = [
        ("not_done", _("Nicht erledigt")),
        ("in_progress", _("In Bearbeitung")),
        ("done", _("Erledigt")),
    ]

    text = models.CharField(verbose_name=_("Titel"), max_length=50)
    status = models.CharField(
        verbose_name=_("Status"),
        max_length=20,
        choices=STATUS,
        default="not_done",
    )

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_("Benutzer")
    )

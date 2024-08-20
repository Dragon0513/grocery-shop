from django.db import models
from django.utils.translation import gettext as _


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

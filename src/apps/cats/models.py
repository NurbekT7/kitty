from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import User

class Breeds(models.Model):
    name = models.CharField(
        _("Порода"),
        max_length=150
    )
    img = models.ImageField(
        _("Изображение"),
        upload_to="images/breeds/"
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = _("Порода")
        verbose_name_plural = _("Породы")

    def __str__(self):
        return self.name


class Cats(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        # editable=False
    )
    breed = models.ForeignKey(
        to="Breeds",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("Порода")
    )
    name = models.CharField(
        _("Имя"),
        max_length=150
    )
    color = models.CharField(
        _("Цвет")
    )
    age = models.DateField(
        _("Дата рождения")
    )
    description = models.TextField(
        _("Описание")
    )
    img = models.ImageField(
        _("Изображение"),
        upload_to="images/cats/"
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = _("Котенок")
        verbose_name_plural = _("Котенки")


    def __str__(self):
        return self.name

    # @property
    # def average_rating(self):
    #     ratings = self.catrating_set.all()
    #     if ratings.exists():
    #         return ratings.aggregate(models.Avg('rating'))['rating__avg']
    #     return None


class CatRating(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name=_("Пользователь"),
        null=True
    )
    cat = models.ForeignKey(
        to=Cats,
        on_delete=models.CASCADE,
        verbose_name=_("Котенок")
    )
    rating = models.PositiveSmallIntegerField(
        _("Рейтинг"),
        choices=[(i, str(i)) for i in range(1, 6)]
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ('user', 'cat')

    def __str__(self):
        return f"{self.user} rated {self.cat} with {self.rating}"

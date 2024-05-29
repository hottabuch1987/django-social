from account.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models



class Review(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews_written", verbose_name="Пользователь"
    )
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews", verbose_name="Кем написано"
    )
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1),
                                                          MaxValueValidator(5)], verbose_name="Рeйтинг")
    content = models.TextField("Текст отзыва")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        

    def __str__(self):
        return f"{self.created_by} о человеке: {self.user}"
    


from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='')
    description = models.TextField(null=True)
    cost = models.FloatField(null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def rating(self):
        reviews = Review.objects.filter(product_id=self)
        sum_ = 0
        for i in reviews:
            sum_ += int(i.stars)
        try:
            return sum_/reviews.count()
        except:
            return 0


STARS = (
    (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)
)
class Review(models.Model):
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    text = models.TextField(null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    stars = models.IntegerField(choices=STARS, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return self.text


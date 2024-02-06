from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"

class Phrase(models.Model):
    phrase = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phrase + "|" + self.category.name
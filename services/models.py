from django.db import models
from category.models import Category

# Create your models here.
class Service(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="services/images", blank=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    service_fee = models.IntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.title

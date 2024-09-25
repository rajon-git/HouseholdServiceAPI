from django.db import models
from django.contrib.auth.models import User
from services.models import Service 

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ManyToManyField(Service)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.service.title} in {self.user.first_name}'s cart"

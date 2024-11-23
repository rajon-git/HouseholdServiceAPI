from django.db import models
from django.contrib.auth.models import User
from cart.models import Cart, CartItem
from services.models import Service

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('accept', 'Accept'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled')
    ], default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    name = models.CharField(max_length=255, default='Dhaka')
    phone = models.CharField(max_length=15, default='Dhaka')
    house = models.CharField(max_length=255, default='Dhaka')
    road = models.CharField(max_length=255, default='Dhaka')
    ward = models.CharField(max_length=255, default='Dhaka')
    city = models.CharField(max_length=255, default="Dhaka")
    state = models.CharField(max_length=255, default='Dhaka')
    payment_type = models.CharField(max_length=20, choices=[
        ('cash', 'Cash'),
        ('bkash', 'Bkash'),
        ('credit', 'Credit Card'),
    ], default='cash')

    def __str__(self):
        return f"Order {self.id} - {self.user.username if self.user else 'Guest'}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def get_total_price(self):
        return self.service.service_fee * self.quantity

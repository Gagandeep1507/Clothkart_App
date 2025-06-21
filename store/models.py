from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    category = models.ForeignKey(Category , on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=8 , decimal_places=2)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name
    

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user
    
    def total_price(self):
        return sum(item.subtotal() for item in self.items.all())
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart , related_name= 'items' , on_delete=models.CASCADE)
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return f"{self.quantity} * {self.product.name}"
    
class Order(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=6 , decimal_places=2)
    status = models.CharField(max_length=20 , default= 'pending')

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
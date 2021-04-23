from django.db import models

from account.models import MyUser
from main.models import Post


class Cart(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='cart')


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitem')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='cartitem')
    amount = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.post.name

    def get_total_price(self):
        return self.post.price * self.amount
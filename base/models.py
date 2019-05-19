from django.contrib.auth.models import User
from django.db import models
import datetime


class UserProfile(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, default=1)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=11)
    photo = models.CharField(max_length=1000, default='')


class Product(models.Model):
    name = models.CharField(max_length=255)
    preview_describe = models.CharField(max_length=120, default="")
    describe = models.CharField(max_length=5000)
    price = models.IntegerField(default=0)
    tags = models.CharField(max_length=3000, default='')
    photo = models.CharField(max_length=3000, default='')
    is_distributing = models.BooleanField(default=1)


class Comment(models.Model):
    author = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, default=0)
    product = models.ForeignKey(to=Product, on_delete=models.SET_NULL, default=0, null=True)
    text = models.CharField(max_length=255)


class ProductTags(models.Model):
    tag_name = models.CharField(max_length=50)
    type = models.CharField(max_length=50, default="")


class Orders(models.Model):
    customer = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, default=0)
    product = models.ForeignKey(to=Product, on_delete=models.SET_NULL, default=0, null=True)
    count = models.IntegerField(default=1)
    size = models.FloatField(default=0)
    phone = models.CharField(default="", max_length=12)
    time = models.DateTimeField(default=datetime.datetime.now())
    price = models.FloatField(default=0)

    STATUS = (
        ('p', 'Processing'),
        ('a', 'Accept'),
        ('d', 'Done'),
        ('c', 'Cancelled')
    )

    status = models.CharField(max_length=1, choices=STATUS, default='p')


class AdminProfile(models.Model):
    user = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, default=0)
    """
      permissions
    """
    see_products_panel = models.BooleanField()
    can_create_products = models.BooleanField()
    can_edit_products = models.BooleanField()
    #
    see_orders_panel = models.BooleanField()
    can_check_orders_info = models.BooleanField()
    can_edit_orders = models.BooleanField()
    #
    see_comments_panel = models.BooleanField()
    can_delete_comments = models.BooleanField()
    #
    see_admins_panel = models.BooleanField()
    can_delete_admins = models.BooleanField()
    can_create_admins = models.BooleanField()




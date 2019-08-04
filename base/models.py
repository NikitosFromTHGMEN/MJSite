from django.contrib.auth.models import User
from django.db import models
import datetime


class UserProfile(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, default=1)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=11)
    photo = models.CharField(max_length=1000, default='')
    is_banned = models.BooleanField(default=False)
    ban_reason = models.CharField(default="", max_length=1000)
    is_reported = models.IntegerField(default=0)
    report_text = models.TextField(default="", max_length="1000")


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
    time = models.DateTimeField(default=datetime.datetime.now())


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
    customer_status = models.CharField(max_length=1, default="n")
    customer_wishes = models.TextField(max_length=1000, default="")
    cancel_reason = models.CharField(max_length=1000, default="")


class Comment1(models.Model):
    author = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, default=0)
    product = models.ForeignKey(to=Product, on_delete=models.SET_NULL, default=0, null=True)
    text = models.CharField(max_length=255)
    time = models.DateTimeField(default=datetime.datetime.now())
    order = models.ForeignKey(to=Orders, on_delete=models.SET_NULL, default=1, null=True)


class AdminProfile(models.Model):
    user = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, default=0)
    """
      permissions
    """
    see_products_panel = models.BooleanField(default=False)
    can_create_products = models.BooleanField(default=False)
    can_edit_products = models.BooleanField(default=False)
    can_remove_products = models.BooleanField(default=False)
    can_distribute_products = models.BooleanField(default=False)
    #
    see_orders_panel = models.BooleanField(default=False)
    can_check_orders_info = models.BooleanField(default=False)
    can_edit_orders = models.BooleanField(default=False)
    #
    see_comments_panel = models.BooleanField(default=False)
    can_delete_comments = models.BooleanField(default=False)
    #
    see_admins_panel = models.BooleanField(default=False)
    can_ban_users = models.BooleanField(default=False)
    can_create_admins = models.BooleanField(default=False)
    can_demote_admins = models.BooleanField(default=False)
    can_edit_products_section = models.BooleanField(default=False)
    can_edit_orders_section = models.BooleanField(default=False)
    can_edit_comments_section = models.BooleanField(default=False)
    can_edit_admins_section = models.BooleanField(default=False)

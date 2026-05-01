from django.db import models
from django.contrib.postgres.fields import ArrayField


class User(models.Model):
    google_id = models.CharField(max_length=255, unique=True)
    email = models.EmailField()
    name = models.CharField(max_length=255)
    picture = models.URLField(blank=True, default='')
    password_hash = models.CharField(max_length=255, blank=True, default='')
    phone = models.CharField(max_length=20, blank=True, null=True)
    whatsapp_optin = models.BooleanField(default=False)
    synced_providers = ArrayField(models.CharField(max_length=50), default=list, blank=True)

    class Meta:
        db_table = 'users'


class Expense(models.Model):
    user = models.ForeignKey(User, to_field='google_id', db_column='user_id', on_delete=models.CASCADE)
    description = models.TextField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(max_length=50, default='Other')
    date = models.DateField()
    product_name = models.TextField(blank=True, default='')
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    size = models.CharField(max_length=50, blank=True, null=True)
    mrp = models.DecimalField(max_digits=12, decimal_places=2, null=True)

    class Meta:
        db_table = 'expenses'
        ordering = ['-date', '-id']


class Budget(models.Model):
    user = models.ForeignKey(User, to_field='google_id', db_column='user_id', on_delete=models.CASCADE)
    month = models.CharField(max_length=7)  # YYYY-MM
    salary = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    budget = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        db_table = 'budgets'
        unique_together = ('user', 'month')


class PushSubscription(models.Model):
    user = models.ForeignKey(User, to_field='google_id', db_column='user_id', on_delete=models.CASCADE)
    subscription = models.TextField()

    class Meta:
        db_table = 'push_subscriptions'
        unique_together = ('user', 'subscription')

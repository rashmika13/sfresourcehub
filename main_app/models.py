from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Resource(models.Model):
    resource_name = models.CharField(max_length=100)
    org_name = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=100, blank=True)
    hours = models.TimeField()
    notes = models.TextField(max_length=250, blank=True)
    street = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    phone = models.IntegerField(blank=True, default=123456789)
    long = models.DecimalField(max_digits=12, decimal_places=6, default=0.000)
    lat = models.DecimalField(max_digits=12, decimal_places=6, default=0.000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.CharField(max_length=200, blank=True)

    def get_absolute_url(self):
        return reverse('detail', kwargs={'resource_id': self.id})

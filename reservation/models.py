from django.conf import settings
from django.db import models

class Table(models.Model):
    seats = models.IntegerField()
    available = models.BooleanField(default=True)

class Reservation(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE, blank=True, null=True)
    seats_reserved = models.IntegerField()
    cost = models.IntegerField()

    def __str__(self):
        return f"reservation of {self.seats_reserved} seats by {self.user}"
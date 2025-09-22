from django.db import models #this was the only line in this file initially

# Create your models here.
class Supplier(models.Model):
    name = models.CharField(max_length=255)
    material = models.CharField(max_length=255)
    contact = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class InventoryItem(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # category = models.CharField(max_length=255, null=True, blank = True)
    
    total_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)  # Added field for total cost
    created_at = models.DateTimeField(auto_now_add=True)

    #following method for total cost calculation by *ALTERNATIVE APPROACH
    def total_cost(self):
        return self.quantity * self.price

    def __str__(self):
        return self.name
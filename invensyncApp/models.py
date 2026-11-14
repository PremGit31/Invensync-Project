from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q


class Supplier(models.Model):
    name = models.CharField(max_length=255)
    material = models.CharField(max_length=255)
    contact = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class InventoryItem(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    supplier = models.ForeignKey(
        Supplier,
        related_name="items",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    reorder_level = models.PositiveIntegerField(
        default=5,
        validators=[MinValueValidator(0)],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name", "pk"]
        constraints = [
            models.CheckConstraint(
                check=Q(price__gte=0),
                name="inventory_price_nonnegative",
            ),
        ]

    @property
    def total_cost(self):
        return self.quantity * self.price

    def __str__(self):
        return self.name


class InventoryMovement(models.Model):
    item = models.ForeignKey(
        InventoryItem,
        related_name="movements",
        on_delete=models.CASCADE,
    )
    quantity_delta = models.IntegerField()
    quantity_after = models.PositiveIntegerField()
    reason = models.CharField(max_length=32, default="Adjustment")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-pk"]

    def __str__(self):
        return f"{self.item.name}: {self.quantity_delta:+d}"

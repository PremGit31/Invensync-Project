from decimal import Decimal

from django import forms

from .models import InventoryItem, Supplier


class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ["name", "quantity", "price", "supplier", "reorder_level"]
        labels = {
            "name": "Item name",
            "quantity": "Quantity in stock",
            "price": "Unit price",
            "supplier": "Supplier",
            "reorder_level": "Low-stock threshold",
        }
        help_texts = {
            "reorder_level": "Show a low-stock alert when quantity reaches this level.",
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "e.g. Cotton canvas"}),
            "quantity": forms.NumberInput(attrs={"min": 0, "step": 1}),
            "price": forms.NumberInput(attrs={"min": 0, "step": "0.01"}),
            "supplier": forms.Select(),
            "reorder_level": forms.NumberInput(attrs={"min": 0, "step": 1}),
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if not name:
            raise forms.ValidationError("Enter an item name.")
        return name

    def clean_quantity(self):
        quantity = self.cleaned_data["quantity"]
        if quantity < 0:
            raise forms.ValidationError("Quantity cannot be negative.")
        return quantity

    def clean_price(self):
        price = self.cleaned_data["price"]
        if price < Decimal("0.00"):
            raise forms.ValidationError("Price cannot be negative.")
        return price

    def clean_reorder_level(self):
        reorder_level = self.cleaned_data["reorder_level"]
        if reorder_level < 0:
            raise forms.ValidationError("Low-stock threshold cannot be negative.")
        return reorder_level


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ["name", "material", "contact"]
        labels = {
            "name": "Supplier name",
            "material": "Materials supplied",
            "contact": "Contact number",
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "e.g. Northstar Textiles"}),
            "material": forms.TextInput(attrs={"placeholder": "e.g. Fabric, thread"}),
            "contact": forms.TextInput(attrs={"placeholder": "Phone or email"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        for field in ("name", "material", "contact"):
            value = cleaned_data.get(field)
            if value is not None:
                cleaned_data[field] = value.strip()
                if not cleaned_data[field]:
                    self.add_error(field, "This field cannot be blank.")
        return cleaned_data

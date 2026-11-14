from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .forms import InventoryItemForm
from .models import InventoryItem, InventoryMovement, Supplier


class InventoryFormTests(TestCase):
    def test_negative_quantity_and_price_are_rejected(self):
        form = InventoryItemForm(
            data={
                "name": "Cotton fabric",
                "quantity": "-1",
                "price": "-0.50",
                "supplier": "",
                "reorder_level": "5",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("quantity", form.errors)
        self.assertIn("price", form.errors)


class InventoryWorkflowTests(TestCase):
    def setUp(self):
        self.supplier = Supplier.objects.create(
            name="Northstar Textiles",
            material="Fabric",
            contact="555-0100",
        )

    def test_create_item_links_supplier_and_calculates_stock_value(self):
        response = self.client.post(
            reverse("manage"),
            {
                "name": "Cotton fabric",
                "quantity": "6",
                "price": "2.50",
                "supplier": str(self.supplier.pk),
                "reorder_level": "5",
            },
        )

        item = InventoryItem.objects.get(name="Cotton fabric")
        self.assertRedirects(response, reverse("manage"))
        self.assertEqual(item.supplier, self.supplier)
        self.assertEqual(item.total_cost, Decimal("15.00"))
        movement = InventoryMovement.objects.get(item=item)
        self.assertEqual(movement.quantity_delta, 6)
        self.assertEqual(movement.quantity_after, 6)

    def test_quantity_edits_record_a_signed_movement(self):
        item = InventoryItem.objects.create(
            name="Canvas",
            quantity=8,
            price=Decimal("4.00"),
            supplier=self.supplier,
        )

        response = self.client.post(
            reverse("edit_inventory", args=[item.pk]),
            {
                "name": item.name,
                "quantity": "5",
                "price": "4.00",
                "supplier": str(self.supplier.pk),
                "reorder_level": "5",
            },
        )

        self.assertRedirects(response, reverse("manage"))
        movement = InventoryMovement.objects.get(item=item)
        self.assertEqual(movement.quantity_delta, -3)
        self.assertEqual(movement.quantity_after, 5)

    def test_search_sort_and_pagination_apply_together(self):
        for quantity in range(12):
            InventoryItem.objects.create(
                name=f"Cable {quantity:02d}",
                quantity=quantity,
                price=Decimal("1.00"),
                supplier=self.supplier,
                reorder_level=2,
            )

        response = self.client.get(
            reverse("manage"),
            {
                "q": "Cable",
                "sort": "quantity",
                "order": "desc",
                "page": "2",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["page_obj"].number, 2)
        self.assertEqual(
            [item.quantity for item in response.context["items"]],
            [1, 0],
        )
        self.assertEqual(response.context["page_obj"].paginator.count, 12)

    def test_deletes_require_post_and_supplier_removal_preserves_items(self):
        item = InventoryItem.objects.create(
            name="Canvas",
            quantity=3,
            price=Decimal("4.00"),
            supplier=self.supplier,
        )

        self.assertEqual(
            self.client.get(reverse("delete_inventory", args=[item.pk])).status_code,
            405,
        )
        response = self.client.post(reverse("delete_supplier", args=[self.supplier.pk]))

        self.assertRedirects(response, reverse("suppliers"))
        item.refresh_from_db()
        self.assertIsNone(item.supplier)

    def test_dashboard_summarizes_stock_value_and_low_stock(self):
        low_stock_item = InventoryItem.objects.create(
            name="Low stock item",
            quantity=3,
            price=Decimal("2.00"),
            supplier=self.supplier,
            reorder_level=5,
        )
        InventoryMovement.objects.create(
            item=low_stock_item,
            quantity_delta=3,
            quantity_after=3,
            reason="Initial stock",
        )
        InventoryItem.objects.create(
            name="Healthy item",
            quantity=10,
            price=Decimal("3.00"),
            supplier=self.supplier,
            reorder_level=4,
        )

        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["summary"]["total_items"], 2)
        self.assertEqual(response.context["summary"]["total_stock"], 13)
        self.assertEqual(response.context["summary"]["total_value"], Decimal("36"))
        self.assertEqual(response.context["summary"]["low_stock_count"], 1)
        self.assertEqual(
            response.context["supplier_values"][0].inventory_value,
            Decimal("36"),
        )
        self.assertEqual(len(response.context["stock_activity"]), 7)
        self.assertEqual(response.context["stock_activity"][-1]["change"], 3)

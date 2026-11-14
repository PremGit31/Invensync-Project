from datetime import timedelta

from django.contrib import messages
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Count, DecimalField, ExpressionWrapper, F, Q, Sum
from django.db.models.functions import TruncDate
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import InventoryItemForm, SupplierForm
from .models import InventoryItem, InventoryMovement, Supplier


INVENTORY_PAGE_SIZE = 10
INVENTORY_SORT_FIELDS = {
    "name": "name",
    "quantity": "quantity",
    "price": "price",
    "value": "stock_value",
    "supplier": "supplier__name",
    "updated": "updated_at",
}


def _stock_value_expression():
    return ExpressionWrapper(
        F("quantity") * F("price"),
        output_field=DecimalField(max_digits=15, decimal_places=2),
    )


def _supplier_stock_value_expression():
    return ExpressionWrapper(
        F("items__quantity") * F("items__price"),
        output_field=DecimalField(max_digits=15, decimal_places=2),
    )


def dashboard(request):
    summary = InventoryItem.objects.aggregate(
        total_items=Count("pk"),
        total_stock=Sum("quantity"),
        total_value=Sum(_stock_value_expression()),
        low_stock_count=Count(
            "pk",
            filter=Q(quantity__lte=F("reorder_level")),
        ),
    )
    summary["total_stock"] = summary["total_stock"] or 0
    summary["total_value"] = summary["total_value"] or 0

    low_stock_items = (
        InventoryItem.objects.select_related("supplier")
        .filter(quantity__lte=F("reorder_level"))
        .order_by("quantity", "name")[:5]
    )
    recent_items = InventoryItem.objects.select_related("supplier").order_by(
        "-updated_at", "-pk"
    )[:5]
    today = timezone.localdate()
    first_day = today - timedelta(days=6)
    daily_changes = (
        InventoryMovement.objects.filter(created_at__date__gte=first_day)
        .annotate(day=TruncDate("created_at"))
        .values("day")
        .annotate(net_change=Sum("quantity_delta"))
        .order_by("day")
    )
    changes_by_day = {
        row["day"]: row["net_change"] or 0 for row in daily_changes
    }
    activity_values = []
    for offset in range(7):
        day = first_day + timedelta(days=offset)
        activity_values.append((day, changes_by_day.get(day, 0)))
    max_daily_change = max((abs(change) for _, change in activity_values), default=0)
    stock_activity = []
    for day, change in activity_values:
        stock_activity.append(
            {
                "day_label": day.strftime("%a"),
                "date_label": day.strftime("%b %d"),
                "change": change,
                "height": round(abs(change) / max_daily_change * 100)
                if max_daily_change
                else 0,
                "direction": "positive" if change > 0 else "negative",
            }
        )

    supplier_values = list(
        Supplier.objects.annotate(
            inventory_value=Sum(_supplier_stock_value_expression()),
        )
        .filter(inventory_value__isnull=False)
        .order_by("-inventory_value", "name")[:5]
    )
    max_supplier_value = max(
        (supplier.inventory_value for supplier in supplier_values),
        default=0,
    )
    for supplier in supplier_values:
        supplier.value_share = (
            round(supplier.inventory_value / max_supplier_value * 100)
            if max_supplier_value
            else 0
        )

    return render(
        request,
        "dashboard.html",
        {
            "summary": summary,
            "low_stock_items": low_stock_items,
            "recent_items": recent_items,
            "stock_activity": stock_activity,
            "supplier_values": supplier_values,
            "active_page": "dashboard",
        },
    )


def manage(request):
    if request.method == "POST":
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                item = form.save()
                if item.quantity:
                    InventoryMovement.objects.create(
                        item=item,
                        quantity_delta=item.quantity,
                        quantity_after=item.quantity,
                        reason="Initial stock",
                    )
            messages.success(request, f"{item.name} was added to inventory.")
            return redirect("manage")
    else:
        form = InventoryItemForm()

    search = request.GET.get("q", "").strip()
    supplier_id = request.GET.get("supplier", "").strip()
    stock_status = request.GET.get("stock", "").strip()
    requested_sort = request.GET.get("sort", "name")
    sort_by = requested_sort if requested_sort in INVENTORY_SORT_FIELDS else "name"
    order = request.GET.get("order", "asc")
    sort_field = INVENTORY_SORT_FIELDS.get(sort_by, "name")
    if order not in {"asc", "desc"}:
        order = "asc"

    items = InventoryItem.objects.select_related("supplier").annotate(
        stock_value=_stock_value_expression()
    )
    if search:
        items = items.filter(
            Q(name__icontains=search) | Q(supplier__name__icontains=search)
        )
    if supplier_id.isdigit():
        items = items.filter(supplier_id=int(supplier_id))
    if stock_status == "low":
        items = items.filter(quantity__gt=0, quantity__lte=F("reorder_level"))
    elif stock_status == "out":
        items = items.filter(quantity=0)
    elif stock_status == "healthy":
        items = items.filter(quantity__gt=F("reorder_level"))

    prefix = "-" if order == "desc" else ""
    items = items.order_by(f"{prefix}{sort_field}", "pk")
    page_obj = Paginator(items, INVENTORY_PAGE_SIZE).get_page(request.GET.get("page"))

    query = request.GET.copy()
    page_urls = {}
    for label, page_number in (
        ("previous", page_obj.previous_page_number() if page_obj.has_previous() else None),
        ("next", page_obj.next_page_number() if page_obj.has_next() else None),
    ):
        if page_number is not None:
            query["page"] = page_number
            page_urls[label] = query.urlencode()

    sort_urls = {}
    for key in INVENTORY_SORT_FIELDS:
        sort_query = request.GET.copy()
        next_order = "desc" if sort_by == key and order == "asc" else "asc"
        sort_query["sort"] = key
        sort_query["order"] = next_order
        sort_query.pop("page", None)
        sort_urls[key] = sort_query.urlencode()

    return render(
        request,
        "manage.html",
        {
            "form": form,
            "page_obj": page_obj,
            "items": page_obj.object_list,
            "search": search,
            "selected_supplier": supplier_id,
            "stock_status": stock_status,
            "suppliers": Supplier.objects.order_by("name"),
            "sort_by": sort_by,
            "order": order,
            "sort_urls": sort_urls,
            "page_urls": page_urls,
            "active_page": "inventory",
        },
    )


def edit_inventory(request, item_id):
    item = get_object_or_404(InventoryItem, pk=item_id)
    if request.method == "POST":
        previous_quantity = item.quantity
        form = InventoryItemForm(request.POST, instance=item)
        if form.is_valid():
            with transaction.atomic():
                item = form.save()
                if item.quantity != previous_quantity:
                    InventoryMovement.objects.create(
                        item=item,
                        quantity_delta=item.quantity - previous_quantity,
                        quantity_after=item.quantity,
                    )
            messages.success(request, f"{item.name} was updated.")
            return redirect("manage")
    else:
        form = InventoryItemForm(instance=item)
    return render(
        request,
        "inventory_form.html",
        {
            "form": form,
            "item": item,
            "active_page": "inventory",
        },
    )


@require_POST
def delete_inventory(request, item_id):
    item = get_object_or_404(InventoryItem, pk=item_id)
    item_name = item.name
    item.delete()
    messages.success(request, f"{item_name} was removed from inventory.")
    return redirect("manage")


def suppliers(request):
    if request.method == "POST":
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = form.save()
            messages.success(request, f"{supplier.name} was added.")
            return redirect("suppliers")
    else:
        form = SupplierForm()

    search = request.GET.get("q", "").strip()
    supplier_list = Supplier.objects.annotate(item_count=Count("items")).order_by("name")
    if search:
        supplier_list = supplier_list.filter(
            Q(name__icontains=search)
            | Q(material__icontains=search)
            | Q(contact__icontains=search)
        )
    return render(
        request,
        "suppliers.html",
        {
            "form": form,
            "suppliers": supplier_list,
            "search": search,
            "active_page": "suppliers",
        },
    )


def edit_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, pk=supplier_id)
    if request.method == "POST":
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            supplier = form.save()
            messages.success(request, f"{supplier.name} was updated.")
            return redirect("suppliers")
    else:
        form = SupplierForm(instance=supplier)
    return render(
        request,
        "supplier_form.html",
        {
            "form": form,
            "supplier": supplier,
            "active_page": "suppliers",
        },
    )


@require_POST
def delete_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, pk=supplier_id)
    supplier_name = supplier.name
    supplier.delete()
    messages.success(
        request,
        f"{supplier_name} was removed. Its inventory items are now unassigned.",
    )
    return redirect("suppliers")


def help(request):
    return render(request, "help.html", {"active_page": "help"})

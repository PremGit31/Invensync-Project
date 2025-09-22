from django.shortcuts import render, redirect, get_object_or_404
from .models import Supplier, InventoryItem
# from .forms import InventoryItemForm
from django.http import HttpResponse

# Create your views here.

def dashboard(request):
    #following for dataase connection test
    # Calculate total items and total inventory value
    inventory_items = InventoryItem.objects.all()
    total_items = inventory_items.count()
    total_inventory_value = sum(item.quantity * item.price for item in inventory_items)

    # Pass the calculated values to the template
    context = {
        'total_items': total_items,
        'total_inventory_value': total_inventory_value,
    }
    return render(request, 'dashboard.html', context)
    #return render(request, 'dashboard.html') #was the only line

# def manage(request): #THIS WAS ORIGINAL WITHOUT SORTING METHODS
#     #this code was added to test the connection with the database
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         quantity = int(request.POST.get('quantity'))
#         price = float(request.POST.get('price'))
#         InventoryItem.objects.create(name=name, quantity=quantity, price=price)
#         return redirect('manage')

#     inventory_items = InventoryItem.objects.all()
#     return render(request, 'manage.html', {'inventory_items': inventory_items})
#     #return render(request, 'manage.html')#this was the initially the only line of code of this function

from django.shortcuts import render, redirect
from .models import InventoryItem

def manage(request):
    # Handle form submission for adding new inventory items
    if request.method == 'POST':
        name = request.POST.get('name')
        quantity = int(request.POST.get('quantity'))
        price = float(request.POST.get('price'))
        InventoryItem.objects.create(name=name, quantity=quantity, price=price)
        return redirect('manage')

    # Get the sorting criteria from the query parameters
    sort_by = request.GET.get('sort_by', 'name')  # Default sort by 'name'
    order = request.GET.get('order', 'asc')  # Default order is ascending

    # Fetch all inventory items
    inventory_items = list(InventoryItem.objects.all())

    # Handle sorting
    if sort_by == 'total_cost':
        # Sort by calculated total cost (quantity * price) in Python
        reverse = (order == 'desc')  # Reverse for descending order
        inventory_items.sort(key=lambda x: x.quantity * x.price, reverse=reverse)
    else:
        # Sort by database fields (e.g., price, quantity, created_at)
        if order == 'desc':
            sort_by = f'-{sort_by}'
        inventory_items = InventoryItem.objects.all().order_by(sort_by)

    # Calculate total cost for each item (for display purposes)
    for item in inventory_items:
        item.total_cost = item.quantity * item.price

    return render(request, 'manage.html', {'inventory_items': inventory_items})


def suppliers(request):
    #this code was added to test the connection with the database
    if request.method == 'POST':
        name = request.POST.get('name')
        material = request.POST.get('material')
        contact = request.POST.get('contact')
        Supplier.objects.create(name=name, material=material, contact=contact)
        return redirect('suppliers')

    suppliers = Supplier.objects.all()
    return render(request, 'suppliers.html', {'suppliers': suppliers})
    #return render(request, 'suppliers.html') #this was the initially the only line of code of this function

def help(request):
    return render(request, 'help.html')

#THE FOLLOWING FOR EDIT AND DELETE BUTTONS

# Edit Supplier
def edit_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)
    if request.method == 'POST':
        supplier.name = request.POST.get('name')
        supplier.material = request.POST.get('material')
        supplier.contact = request.POST.get('contact')
        supplier.save()
        return redirect('suppliers')
    return render(request, 'edit_supplier.html', {'supplier': supplier})

# Delete Supplier
def delete_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)
    supplier.delete()
    return redirect('suppliers')

# Edit Inventory Item
def edit_inventory(request, item_id):
    item = get_object_or_404(InventoryItem, id=item_id)
    if request.method == 'POST':
        item.name = request.POST.get('name')
        item.quantity = int(request.POST.get('quantity'))
        item.price = float(request.POST.get('price'))
        item.save()
        return redirect('manage')
    return render(request, 'edit_inventory.html', {'item': item})

# Delete Inventory Item
def delete_inventory(request, item_id):
    item = get_object_or_404(InventoryItem, id=item_id)
    item.delete()
    return redirect('manage')
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('manage/', views.manage, name='manage'),
    path('manage/edit/<int:item_id>/', views.edit_inventory, name='edit_inventory'), #FOR ADD AND EDIT
    path('manage/delete/<int:item_id>/', views.delete_inventory, name='delete_inventory'),#FOR ADD AND EDIT
    path('suppliers/', views.suppliers, name='suppliers'),
    path('suppliers/edit/<int:supplier_id>/', views.edit_supplier, name='edit_supplier'),#FOR ADD AND EDIT
    path('suppliers/delete/<int:supplier_id>/', views.delete_supplier, name='delete_supplier'),#FOR ADD AND EDIT
    path('help/',views.help,name='help'),
]
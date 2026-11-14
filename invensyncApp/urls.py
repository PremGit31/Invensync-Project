from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('manage/', views.manage, name='manage'),
    path('manage/edit/<int:item_id>/', views.edit_inventory, name='edit_inventory'),
    path('manage/delete/<int:item_id>/', views.delete_inventory, name='delete_inventory'),
    path('suppliers/', views.suppliers, name='suppliers'),
    path('suppliers/edit/<int:supplier_id>/', views.edit_supplier, name='edit_supplier'),
    path('suppliers/delete/<int:supplier_id>/', views.delete_supplier, name='delete_supplier'),
    path('help/', views.help, name='help'),
]
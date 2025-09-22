InvenSync
InvenSync is a Django-based inventory management system designed to streamline inventory and supplier management. It provides an intuitive interface for managing inventory items, tracking suppliers, and monitoring stock levels. The project is built with Django and integrates MySQL as the database backend.

Features
1. Dashboard
Displays an overview of the inventory.
Shows total items and total inventory value.
Provides a summary of inventory statistics.
2. Inventory Management
Add, edit, and delete inventory items.
Sort inventory items by various criteria such as price, quantity, total cost, and creation time.
Calculate and display the total cost of each inventory item.
3. Supplier Management
Add, edit, and delete suppliers.
Manage supplier details such as name, material, and contact information.
4. Help & Support
Provides guidance on using the system.
Displays contact information for support.
Project Structure
1. Django Project: InventProject
Contains the main project configuration files:
settings.py: Configures the database, installed apps, and static files.
urls.py: Routes URLs to the appropriate app.
wsgi.py and asgi.py: Deployment configurations.
2. Django App: invensyncApp
Contains the core functionality of the project:
views.py: Handles the logic for rendering templates and processing requests.
models.py: Defines the database models for Supplier and InventoryItem.
urls.py: Maps URLs to views.
templates/: Contains HTML templates for the user interface.
static/: Contains CSS and JavaScript files for styling and interactivity.

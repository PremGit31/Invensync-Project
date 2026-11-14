InvenSync
InvenSync is a Django-based inventory management system designed to streamline inventory and supplier management. It provides an intuitive interface for managing inventory items, tracking suppliers, and monitoring stock levels. The project is built with Django and integrates MySQL as the database backend.

Local Setup (Windows)
1. Create and activate a virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
2. Install the project dependencies:
   ```powershell
   python -m pip install -r requirements.txt
   ```
3. Ensure the MySQL server is running and create the database:
   ```sql
   CREATE DATABASE inventory_mysqldb CHARACTER SET utf8mb4;
   ```
4. Configure the MySQL connection in PowerShell (use your own database password):
   ```powershell
   $env:MYSQL_DATABASE = "inventory_mysqldb"
   $env:MYSQL_USER = "root"
   $env:MYSQL_PASSWORD = "your-local-mysql-password"
   ```
   For production, also set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`, and
   `DJANGO_ALLOWED_HOSTS` to the appropriate secure values.
5. Apply migrations and start the development server:
   ```powershell
   python manage.py migrate
   python manage.py runserver
   ```

Features
1. Dashboard
   Shows total item count, total stock, inventory value, low-stock alerts,
   recent item updates, supplier value distribution, and seven-day stock changes.
2. Inventory Management
   Create, edit, and delete items; track quantity, unit price, supplier, and
   reorder level; search, filter, sort, and paginate the inventory list.
3. Supplier Management
   Create, update, search, and delete supplier records linked to inventory items.
4. Validation and history
   Prevents negative quantities and prices and records quantity adjustments
   for the dashboard's stock activity view.
5. Responsive interface
   Provides a shared navigation layout for desktop and mobile screens.
Project Structure
1. Django Project: InventProject
Contains the main project configuration files:
settings.py: Configures the database, installed apps, and static files.
urls.py: Routes URLs to the appropriate app.
wsgi.py and asgi.py: Deployment configurations.
2. Django App: invensyncApp
Contains the core functionality of the project:
views.py: Handles the logic for rendering templates and processing requests.
models.py: Defines Supplier, InventoryItem, and InventoryMovement.
forms.py: Validates inventory and supplier input.
urls.py: Maps URLs to views.
templates/: Contains HTML templates for the user interface.
static/: Contains CSS and JavaScript files for styling and interactivity.

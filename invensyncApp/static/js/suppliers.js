document.addEventListener("DOMContentLoaded", function () {
    const addItemBtn = document.getElementById("addItemBtn");
    const itemName = document.getElementById("itemName");
    const itemQuantity = document.getElementById("itemQuantity");
    const itemPrice = document.getElementById("itemPrice");
    const tableBody = document.querySelector("#inventoryTable tbody");

    if (!addItemBtn || !tableBody) {
        console.error("Required elements not found.");
        return;
    }

    loadSuppliers();

    addItemBtn.addEventListener("click", function () {
        const supplierName = itemName.value.trim();
        const material = itemQuantity.value.trim();
        const contact = itemPrice.value.trim();

        if (supplierName && material && contact) {
            const supplier = { name: supplierName, material: material, contact: contact };
            addSupplierToTable(supplier);
            saveSupplierToLocalStorage(supplier);
            itemName.value = "";
            itemQuantity.value = "";
            itemPrice.value = "";
        }
    });

    function addSupplierToTable(supplier) {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td class="name-cell">${supplier.name}</td>
            <td class="material-cell">${supplier.material}</td>
            <td class="contact-cell">${supplier.contact}</td>
            <td>
                <button class="edit-btn">Edit</button>
                <button class="delete-btn">Delete</button>
            </td>
        `;

        tableBody.appendChild(row);

        // Delete functionality
        row.querySelector(".delete-btn").addEventListener("click", function () {
            row.remove();
            removeSupplierFromLocalStorage(supplier);
        });

        // Edit functionality
        row.querySelector(".edit-btn").addEventListener("click", function () {
            editSupplier(row, supplier);
        });
    }

    function editSupplier(row, supplier) {
        const nameCell = row.querySelector(".name-cell");
        const materialCell = row.querySelector(".material-cell");
        const contactCell = row.querySelector(".contact-cell");

        // Create input fields for editing
        nameCell.innerHTML = `<input type="text" value="${supplier.name}">`;
        materialCell.innerHTML = `<input type="text" value="${supplier.material}">`;
        contactCell.innerHTML = `<input type="text" value="${supplier.contact}">`;

        // Change Edit button to Save
        const editButton = row.querySelector(".edit-btn");
        editButton.textContent = "Save";
        editButton.classList.add("save-btn");

        editButton.removeEventListener("click", editSupplier);
        editButton.addEventListener("click", function () {
            saveEditedSupplier(row, supplier);
        });
    }

    function saveEditedSupplier(row, oldSupplier) {
        const nameCell = row.querySelector(".name-cell input");
        const materialCell = row.querySelector(".material-cell input");
        const contactCell = row.querySelector(".contact-cell input");

        const updatedSupplier = {
            name: nameCell.value.trim(),
            material: materialCell.value.trim(),
            contact: contactCell.value.trim()
        };

        // Update table cells
        row.querySelector(".name-cell").textContent = updatedSupplier.name;
        row.querySelector(".material-cell").textContent = updatedSupplier.material;
        row.querySelector(".contact-cell").textContent = updatedSupplier.contact;

        // Restore Edit button
        const saveButton = row.querySelector(".save-btn");
        saveButton.textContent = "Edit";
        saveButton.classList.remove("save-btn");

        saveButton.removeEventListener("click", saveEditedSupplier);
        saveButton.addEventListener("click", function () {
            editSupplier(row, updatedSupplier);
        });

        // Update localStorage
        updateSupplierInLocalStorage(oldSupplier, updatedSupplier);
    }

    function saveSupplierToLocalStorage(supplier) {
        const suppliers = JSON.parse(localStorage.getItem("suppliers")) || [];
        suppliers.push(supplier);
        localStorage.setItem("suppliers", JSON.stringify(suppliers));
    }

    function loadSuppliers() {
        tableBody.innerHTML = "";
        const suppliers = JSON.parse(localStorage.getItem("suppliers")) || [];
        suppliers.forEach(addSupplierToTable);
    }

    function removeSupplierFromLocalStorage(supplier) {
        let suppliers = JSON.parse(localStorage.getItem("suppliers")) || [];
        suppliers = suppliers.filter(s => s.name !== supplier.name || s.material !== supplier.material || s.contact !== supplier.contact);
        localStorage.setItem("suppliers", JSON.stringify(suppliers));
    }

    function updateSupplierInLocalStorage(oldSupplier, newSupplier) {
        let suppliers = JSON.parse(localStorage.getItem("suppliers")) || [];
        const index = suppliers.findIndex(s => s.name === oldSupplier.name && s.material === oldSupplier.material && s.contact === oldSupplier.contact);

        if (index !== -1) {
            suppliers[index] = newSupplier;
            localStorage.setItem("suppliers", JSON.stringify(suppliers));
        }
    }
});

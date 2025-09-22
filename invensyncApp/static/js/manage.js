// document.addEventListener("DOMContentLoaded", function () {
//     let inventoryData = JSON.parse(localStorage.getItem("inventoryData")) || [];
//     let totalItems = 0;
//     let lowStockItems = 0;
//     let totalInventoryValue = 0;

//     const totalItemsSpan = document.getElementById("total-items");
//     const lowStockSpan = document.getElementById("low-stock");
//     const totalValueSpan = document.getElementById("total-value");
//     const addItemBtn = document.getElementById("addItemBtn");
//     const inventoryTable = document.querySelector("#inventoryTable tbody");

//     function updateSummary() {
//         totalItems = inventoryData.length;
//         lowStockItems = inventoryData.filter(item => item.quantity < 5).length;
//         totalInventoryValue = inventoryData.reduce((sum, item) => sum + item.quantity * item.price, 0);

//         totalItemsSpan.textContent = totalItems;
//         lowStockSpan.textContent = lowStockItems;
//         totalValueSpan.textContent = totalInventoryValue.toFixed(2);

//         // Save inventory data to localStorage
//         localStorage.setItem("inventoryData", JSON.stringify(inventoryData));
//         console.log("Inventory data saved to localStorage:", inventoryData); // Debugging
//     }

//     function renderTable() {
//         inventoryTable.innerHTML = ""; // Clear the table
//         inventoryData.forEach((item, index) => {
//             const row = document.createElement("tr");
//             if (item.quantity < 5) {
//                 row.classList.add("low-stock-warning");
//             }

//             row.innerHTML = `
//                 <td>${item.name}</td>
//                 <td>${item.quantity}</td>
//                 <td>${item.price.toFixed(2)}</td>
//                 <td class="total-cost">$${(item.quantity * item.price).toFixed(2)}</td>
//                 <td>
//                     <button class="edit-btn">EDIT</button>
//                     <button class="delete-btn">DELETE</button>
//                 </td>
//             `;

//             // Edit functionality
//             row.querySelector(".edit-btn").addEventListener("click", function () {
//                 const newName = prompt("Enter new name:", item.name);
//                 const newQuantity = parseInt(prompt("Enter new quantity:", item.quantity));
//                 const newPrice = parseFloat(prompt("Enter new price:", item.price));

//                 if (!newName || isNaN(newQuantity) || isNaN(newPrice) || newQuantity <= 0 || newPrice <= 0) {
//                     alert("Please enter valid item details!");
//                     return;
//                 }

//                 // Update item
//                 item.name = newName;
//                 item.quantity = newQuantity;
//                 item.price = newPrice;

//                 renderTable();
//                 updateSummary();
//             });

//             // Delete functionality
//             row.querySelector(".delete-btn").addEventListener("click", function () {
//                 inventoryData.splice(index, 1); // Remove item from array
//                 renderTable();
//                 updateSummary();
//             });

//             inventoryTable.appendChild(row);
//         });
//     }

//     addItemBtn.addEventListener("click", function () {
//         const itemName = document.getElementById("itemName").value.trim();
//         const itemQuantity = parseInt(document.getElementById("itemQuantity").value);
//         const itemPrice = parseFloat(document.getElementById("itemPrice").value);

//         if (!itemName || isNaN(itemQuantity) || isNaN(itemPrice) || itemQuantity <= 0 || itemPrice <= 0) {
//             alert("Please enter valid item details!");
//             return;
//         }

//         // Add new item to inventory
//         inventoryData.push({
//             name: itemName,
//             quantity: itemQuantity,
//             price: itemPrice
//         });

//         // Clear input fields
//         document.getElementById("itemName").value = "";
//         document.getElementById("itemQuantity").value = "";
//         document.getElementById("itemPrice").value = "";

//         renderTable();
//         updateSummary();
//     });

//     // Initial render
//     renderTable();
//     updateSummary();
// });
document.addEventListener("DOMContentLoaded", function () {
    const totalItemsSpan = document.getElementById("total-items");
    const lowStockSpan = document.getElementById("low-stock");
    const totalValueSpan = document.getElementById("total-value");

    function updateSummary() {
        const inventoryData = JSON.parse(localStorage.getItem("inventoryData")) || [];
        const totalItems = inventoryData.length;
        const lowStockItems = inventoryData.filter(item => item.quantity < 5).length;
        const totalInventoryValue = inventoryData.reduce((sum, item) => sum + item.quantity * item.price, 0);

        totalItemsSpan.textContent = totalItems;
        lowStockSpan.textContent = lowStockItems;
        totalValueSpan.textContent = totalInventoryValue.toFixed(2);
    }

    // Update the summary on page load
    updateSummary();
});
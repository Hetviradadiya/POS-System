document.addEventListener("DOMContentLoaded", function () {
    fetchFoodItems();
});

function fetchFoodItems() {
    fetch("/api/food-items/")  
        .then(response => response.json())
        .then(data => {
            let tableBody = document.getElementById("foodTableBody");
            tableBody.innerHTML = "";
            data.forEach(item => {
                let statusClass = item.status === "Active" ? "status-active" : "status-inactive";
                let row = `
                    <tr>
                        <td>${item.id}</td>
                        <td><img src="${item.image}" alt="${item.name}" class="food-img"></td>
                        <td>${item.name}</td>
                        <td>${item.category}</td>
                        <td>${item.description}</td>
                        <td>$${item.price.toFixed(2)}</td>
                        <td>
                            <select class="status-dropdown ${statusClass}" data-id="${item.id}" onchange="updateStatus(this)">
                                <option value="Active" ${item.status === "Active" ? "selected" : ""}>Active</option>
                                <option value="Inactive" ${item.status === "Inactive" ? "selected" : ""}>Inactive</option>
                            </select>
                        </td>
                    </tr>
                `;
                tableBody.innerHTML += row;
            });
        })
        .catch(error => console.error("Error fetching food items:", error));
}

function updateStatus(selectElement) {
    let foodId = selectElement.getAttribute("data-id");
    let newStatus = selectElement.value;

    fetch(`/api/update-food-status/${foodId}/`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(), 
        },
        body: JSON.stringify({ status: newStatus }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            selectElement.classList.toggle("status-active", newStatus === "Active");
            selectElement.classList.toggle("status-inactive", newStatus === "Inactive");
        } else {
            alert("Failed to update status");
        }
    })
    .catch(error => console.error("Error updating status:", error));
}

function getCSRFToken() {
    return document.cookie.split("; ").find(row => row.startsWith("csrftoken="))?.split("=")[1];
}



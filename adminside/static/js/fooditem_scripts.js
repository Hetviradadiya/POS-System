// search button
function toggleSearch() {
  let searchContainer = document.querySelector(".search-container");
  let searchInput = document.querySelector(".search-input");

  searchContainer.classList.toggle("active");
  if (searchContainer.classList.contains("active")) {
    searchInput.focus();
  }
}

//search function
document.getElementById("searchInput").addEventListener("keyup", function () {
  let filter = this.value.toLowerCase().trim();
  let rows = document.querySelectorAll("#foodTableBody tr");
  let matchFound = false;

  rows.forEach(function (row) {
    if (row.id === "noDataRow") return;

    let food_item = row.cells[2].textContent.toLowerCase();
    console.log(food_item);

    if (food_item.includes(filter)) {
      row.style.display = "";
      matchFound = true;
    } else {
      row.style.display = "none";
    }
  });

  let tableBody = document.getElementById("foodTableBody");
  let noData = document.getElementById("noDataRow");

  if (filter && !matchFound) {
    if (!noData) {
      noData = document.createElement("tr");
      noData.id = "noDataRow";
      noData.innerHTML = `<td colspan="7" style="text-align: center;">No data found</td>`; //add no datafound row
      tableBody.appendChild(noData);
    }
  } else {
    if (noData) {
      noData.remove();
    }
  }

  // if search bar is empty, show all rows again
  if (filter === "") {
    rows.forEach(function (row) {
      row.style.display = "";
    });
    if (noData) {
      noData.remove();
    }
  }
});

document.addEventListener("DOMContentLoaded", function () {
  fetchFoodItems();
});

function fetchFoodItems() {
  fetch("/api/food-items/")
    .then((response) => response.json())
    .then((data) => {
      let tableBody = document.getElementById("foodTableBody");
      tableBody.innerHTML = "";
      data.forEach((item) => {
        let statusClass =
          item.status === "Active" ? "status-active" : "status-inactive";
        let row = `
                    <tr>
                        <td>${item.id}</td>
                        <td><img src="${item.image}" alt="${
          item.name
        }" class="food-img"></td>
                        <td>${item.name}</td>
                        <td>${item.category}</td>
                        <td>${item.description}</td>
                        <td>$${item.price.toFixed(2)}</td>
                        <td>
                            <select class="status-dropdown ${statusClass}" data-id="${
          item.id
        }" onchange="updateStatus(this)">
                                <option value="Active" ${
                                  item.status === "Active" ? "selected" : ""
                                }>Active</option>
                                <option value="Inactive" ${
                                  item.status === "Inactive" ? "selected" : ""
                                }>Inactive</option>
                            </select>
                        </td>
                    </tr>
                `;
        tableBody.innerHTML += row;
      });
    })
    .catch((error) => console.error("Error fetching food items:", error));
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
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        selectElement.classList.toggle("status-active", newStatus === "Active");
        selectElement.classList.toggle(
          "status-inactive",
          newStatus === "Inactive"
        );
      } else {
        alert("Failed to update status");
      }
    })
    .catch((error) => console.error("Error updating status:", error));
}

function getCSRFToken() {
  return document.cookie
    .split("; ")
    .find((row) => row.startsWith("csrftoken="))
    ?.split("=")[1];
}

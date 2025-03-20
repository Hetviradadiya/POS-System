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
  let rows = document.querySelectorAll("#purchaseTableBody tr");
  let matchFound = false;

  rows.forEach(function (row) {
    if (row.id === "noDataRow") return;

    let food_item = row.cells[1].textContent.toLowerCase();

    if (food_item.includes(filter)) {
      row.style.display = "";
      matchFound = true;
    } else {
      row.style.display = "none";
    }
  });

  let tableBody = document.getElementById("purchaseTableBody");
  let noData = document.getElementById("noDataRow");

  if (filter && !matchFound) {
    if (!noData) {
      noData = document.createElement("tr");
      noData.id = "noDataRow";
      noData.innerHTML = `<td colspan="9" style="text-align: center;">No data found</td>`; //add no datafound row
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

// open form
function openForm(isUpdate = false) {
  document.getElementById("overlay").style.display = "block";
  document.getElementById("myForm").style.display = "block";
  document.body.classList.add("popup-open");

  if (!isUpdate) {
    resetForm(); // Clears form
    document.querySelector(".form-container h1").innerText = "Add Details";
    document.querySelector(".form-buttons button[type='submit']").innerText =
      "Add Details";
  }
}

// Close form
function closeForm() {
  document.getElementById("overlay").style.display = "none";
  document.getElementById("myForm").style.display = "none";
  document.body.classList.remove("popup-open");

  resetForm(); // Reset form
  clearErrors(); // Clear validation errors
}

// reset form
function resetForm() {
  document.getElementById("purchaseId").value = "";
  document.getElementById("foodItem").value = "";
  document.getElementById("quantity").value = "";
  document.getElementById("costPrice").value = "";
  document.getElementById("branch").value = "";
  document.getElementById("supplier").value = "";
  document.getElementById("purchaseDate").value = "";
  document.getElementById("paymentStatus").value = "";
}

//Clear validation errors
function clearErrors() {
  document
    .querySelectorAll(".error")
    .forEach((el) => el.classList.remove("error"));
  document.querySelectorAll(".error-message").forEach((el) => el.remove()); // Remove error messages
}

function extractId(value) {
  return value.split(" - ")[0]; // Extracts ID part before " - "
}
function formatDate(dateString) {
  if (!dateString) return ""; // Handle empty date values

  let date = new Date(dateString);
  if (isNaN(date)) return ""; // Handle invalid date

  // Extract YYYY-MM-DD manually to avoid timezone issues
  let year = date.getFullYear();
  let month = String(date.getMonth() + 1).padStart(2, "0"); // Months are 0-based
  let day = String(date.getDate()).padStart(2, "0");

  return `${year}-${month}-${day}`;
}
function editpurchase(
  purchaseId,
  food_item,
  quantity,
  cost_price,
  branch,
  supplier,
  purchased_date,
  payment_status
) {
  document.getElementById("purchaseId").value = purchaseId;
  document.getElementById("foodItem").value = food_item;
  document.getElementById("quantity").value = quantity;
  document.getElementById("costPrice").value = cost_price;
  document.getElementById("purchaseDate").value = formatDate(purchased_date);

  // Extract only the numeric ID
  let branchId = extractId(branch);
  let supplierId = extractId(supplier);

  // Select the correct branch
  let branchSelect = document.getElementById("branch");
  for (let option of branchSelect.options) {
    if (option.value == branchId) {
      option.selected = true;
      break;
    }
  }

  // Select the correct supplier
  let supplierSelect = document.getElementById("supplier");
  for (let option of supplierSelect.options) {
    if (option.value == supplierId) {
      option.selected = true;
      break;
    }
  }

  let statusSelect = document.getElementById("paymentStatus");
  if (payment_status === "Done" || payment_status === "Remain") {
    statusSelect.value = payment_status;
  } else {
    statusSelect.value = "";
  }

  document.querySelector(".form-container h1").innerText = "Update Details";
  document.querySelector(".form-buttons button[type='submit']").innerText =
    "Update Details";

  openForm(true); // Open form for update
}

//form validation
document
  .getElementById("purchaseForm")
  .addEventListener("submit", function (event) {
    let isValid = true;

    function showError(fieldId, message) {
      const field = document.getElementById(fieldId);
      let errorSpan = field.nextElementSibling;

      if (!errorSpan || !errorSpan.classList.contains("error-message")) {
        errorSpan = document.createElement("span");
        errorSpan.classList.add("error-message");
        field.parentNode.appendChild(errorSpan);
      }

      field.classList.add("error");
      errorSpan.textContent = message;
      errorSpan.style.color = "red";
    }

    clearErrors(); // Clear errors

    const foodItem = document.getElementById("foodItem").value.trim();
    if (!foodItem) {
      showError("foodItem", "FoodItem is required!");
      isValid = false;
    }

    const quantity = document.getElementById("quantity").value.trim();
    if (!quantity) {
      showError("quantity", "Quantity is required!");
      isValid = false;
    }

    const costPrice = document.getElementById("costPrice").value.trim();
    if (!costPrice) {
      showError("costPrice", "CostPrice is required!");
      isValid = false;
    }

    const branch = document.getElementById("branch").value;
    if (!branch) {
      showError("branch", "Branch is required!");
      isValid = false;
    }

    const supplier = document.getElementById("supplier").value;
    if (!supplier) {
      showError("supplier", "Supplier is required!");
      isValid = false;
    }

    const purchaseDate = document.getElementById("purchaseDate").value;
    if (!purchaseDate) {
      showError("purchaseDate", "Purchase Date is required!");
      isValid = false;
    }

    const paymentStatus = document.getElementById("paymentStatus").value;
    if (!paymentStatus) {
      showError("paymentStatus", "Payment Status is required!");
      isValid = false;
    }

    if (!isValid) {
      event.preventDefault(); // Prevent form submission if validation fails
      document.getElementById("overlay").style.display = "block"; // Keep the form open
      document.getElementById("myForm").style.display = "block";
    }
  });

//message when try to delete row
function confirmDelete() {
  return confirm(
    "Are you sure you want to delete this category? This action cannot be undone."
  );
}
function confirmDelete(event) {
  event.preventDefault(); // Stop form from submitting immediately

  Swal.fire({
    title: "Are you sure?",
    text: "You won't be able to undo this action!",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#d33",
    cancelButtonColor: "#3085d6",
    confirmButtonText: "Yes, delete it!",
  }).then((result) => {
    if (result.isConfirmed) {
      event.target.submit(); // Submit form if confirmed
    }
  });

  return false; // Prevent default form submission
}

// Auto-hide messages after 3 seconds
setTimeout(function () {
  let alerts = document.querySelectorAll(".custom-alert");
  alerts.forEach((alert) => {
    alert.style.opacity = "0"; // Smooth fade-out
    setTimeout(() => alert.remove(), 500); // Remove after fade-out
  });
}, 3000);

// Close button function
function closeAlert(button) {
  let alert = button.parentElement;
  alert.style.opacity = "0";
  setTimeout(() => alert.remove(), 500);
}

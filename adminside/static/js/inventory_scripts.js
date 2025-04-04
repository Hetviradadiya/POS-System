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

  let tableBody = document.getElementById("foodTableBody");
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

function openCsvUpload(event) {
  event.preventDefault(); // Prevent default button behavior
  document.getElementById("csvForm").style.display = "block";
  document.getElementById("csvOverlay").style.display = "block";
}

function closeCsvUpload() {
  document.getElementById("csvForm").style.display = "none";
  document.getElementById("csvOverlay").style.display = "none";
}

// open form
function openForm(isUpdate = false) {
  document.getElementById("overlay").style.display = "block";
  document.getElementById("myForm").style.display = "block";
  document.body.classList.add("popup-open");

  if (!isUpdate) {
    resetForm(); // Clears form
    document.querySelector(".form-container h1").innerText = "Add Food Item";
    document.querySelector(".form-buttons button[type='submit']").innerText =
      "Add Food Item";
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
  document.getElementById("inventoryId").value = "";
  document.getElementById("itemImage").value = "";
  document.getElementById("foodItem").value = "";
  document.getElementById("category").value = "";
  document.getElementById("itemDescription").value = "";
  document.getElementById("quantity").value = "";
  document.getElementById("branch").value = "";
  document.getElementById("costPrice").value = "";
  document.getElementById("sellPrice").value = "";
  document.getElementById("mfgDate").value = "";
  document.getElementById("expDate").value = "";
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

function editfooditem(
  inventoryId,
  image,
  food_item,
  category,
  description,
  quantity,
  branch,
  cost_price,
  sell_price,
  mfg_date,
  exp_date
) {

  document.getElementById("inventoryId").value = inventoryId;
  if (image) {
    document.getElementById("itemImage").src = image;
  }
  document.getElementById("itemDescription").value = description;
  document.getElementById("quantity").value = quantity;
  document.getElementById("costPrice").value = cost_price;
  document.getElementById("sellPrice").value = sell_price;
  // document.getElementById("mfgDate").value = mfg_date;
  // document.getElementById("expDate").value = exp_date;
  // Format dates properly
  document.getElementById("mfgDate").value = formatDate(mfg_date);
  document.getElementById("expDate").value = formatDate(exp_date);

  // Extract only the numeric ID
  let purchaseId = extractId(food_item);
  let categoryId = extractId(category);
  let branchId = extractId(branch);

  // Select the correct supplier
  let foodItemSelect = document.getElementById("foodItem");
  for (let option of foodItemSelect.options) {
    if (option.value == purchaseId) {
      option.selected = true;
      break;
    }
  }
  // Select the correct supplier
  let categorySelect = document.getElementById("category");
  for (let option of categorySelect.options) {
    if (option.value == categoryId) {
      option.selected = true;
      break;
    }
  }
  // Select the correct branch
  let branchSelect = document.getElementById("branch");
  for (let option of branchSelect.options) {
    if (option.value == branchId) {
      option.selected = true;
      break;
    }
  }

  document.querySelector(".form-container h1").innerText = "Update FoodItem";
  document.querySelector(".form-buttons button[type='submit']").innerText =
    "Update FoodItem";

  openForm(true); // Open form for update
}

//form validation
document
  .getElementById("foodItemForm")
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

  //   let requiredFields = [
  //     { id: "itemImage", message: "FoodItem Image is required!" },
  //     { id: "foodItem", message: "FoodItem is required!" },
  //     { id: "category", message: "Category is required!" },
  //     { id: "itemDescription", message: "Description is required!" },
  //     { id: "quantity", message: "Quantity is required!" },
  //     { id: "branch", message: "Branch is required!" },
  //     { id: "costPrice", message: "CostPrice is required!" },
  //     { id: "sellPrice", message: "SellPrice is required!" },
  //     { id: "mfgDate", message: "MFG Date is required!" },
  //     { id: "expDate", message: "EXP Date is required!" },
  //   ];

  //   requiredFields.forEach(({ id, message }) => {
  //     if (!document.getElementById(id).value.trim()) {
  //       showError(id, message);
  //       isValid = false;
  //     }
  //   });

  //   if (!isValid) {
  //     event.preventDefault();
  //     document.getElementById("overlay").style.display = "block";
  //     document.getElementById("myForm").style.display = "block";
  //   }
  // });

  const itemImage = document.getElementById("itemImage").value.trim();
  if (!itemImage) {
    showError("itemImage", "FoodItem Image is required!");
    isValid = false;
  }

  const foodItem = document.getElementById("foodItem").value.trim();
  if (!foodItem) {
    showError("foodItem", "FoodItem is required!");
    isValid = false;
  }
  const category = document.getElementById("category").value.trim();
  if (!category) {
    showError("category", "Category is required!");
    isValid = false;
  }
  const itemDescription = document
    .getElementById("itemDescription")
    .value.trim();
  if (!itemDescription) {
    showError("itemDescription", "Description is required!");
    isValid = false;
  }

  const quantity = document.getElementById("quantity").value.trim();
  if (!quantity) {
    showError("quantity", "Quantity is required!");
    isValid = false;
  }

  const branch = document.getElementById("branch").value;
  if (!branch) {
    showError("branch", "Branch is required!");
    isValid = false;
  }
  const costPrice = document.getElementById("costPrice").value.trim();
  if (!costPrice) {
    showError("costPrice", "CostPrice is required!");
    isValid = false;
  }
  const sellPrice = document.getElementById("sellPrice").value.trim();
  if (!sellPrice) {
    showError("sellPrice", "SellPrice is required!");
    isValid = false;
  }

  const mfgDate = document.getElementById("mfgDate").value;
  if (!mfgDate) {
    showError("mfgDate", "MFG Date is required!");
    isValid = false;
  }

  const expDate = document.getElementById("expDate").value;

  if (!expDate) {
    showError("expDate", "EXP Date is required!");
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
}, 5000);

// Close button function
function closeAlert(button) {
  let alert = button.parentElement;
  alert.style.opacity = "0";
  setTimeout(() => alert.remove(), 500);
}

function populatePurchaseData() {
  var selectedOption = document.getElementById("foodItem").selectedOptions[0];

  if (selectedOption) {
    document.getElementById("purchaseId").value = selectedOption.value; // Use purchase_id as the value
    document.getElementById("foodItemName").value =
      selectedOption.getAttribute("data-food-item"); // Display food name
    document.getElementById("quantity").value =
      selectedOption.getAttribute("data-quantity");
    document.getElementById("branch").value =
      selectedOption.getAttribute("data-branch");
    document.getElementById("costPrice").value =
      selectedOption.getAttribute("data-cost");
    let mfgDate = selectedOption.getAttribute("data-mfg");
    if (mfgDate) {
      document.getElementById("mfgDate").value = mfgDate;
    }
  }
}

function toggleSearch() {
  let searchContainer = document.querySelector(".search-container");
  let searchInput = document.querySelector(".search-input");

  searchContainer.classList.toggle("active");
  if (searchContainer.classList.contains("active")) {
    searchInput.focus();
  }
}

document.getElementById("searchInput").addEventListener("keyup", function () {
  let filter = this.value.trim().toLowerCase();
  let rows = document.querySelectorAll("#foodTableBody tr");
  
  rows.forEach(function (row) {
    let itemname = row.cells[2].textContent.trim().toLowerCase();
    let category = row.cells[3].textContent.trim().toLowerCase();
    
    if (itemname.includes(filter) || category.includes(filter)) {
      row.style.display = "";
    } else {
      row.style.display = "none";
    }
  });
});

let foodItemId = 1;
let updateIndex = null;

document.addEventListener("DOMContentLoaded", function () {
  document
    .getElementById("foodItemForm").addEventListener("submit", function (event) {
      event.preventDefault();
      if (updateIndex !== null) {
        updateFoodItem();
      } else {
        addFoodItem();
      }
    });
    
    populateStaticDropdowns();
  });
  


function addFoodItem() {
  clearErrors();
  if (!validateForm()) return;
  
  
  let itemName = document.getElementById("itemName");
  let itemCategory = document.getElementById("itemCategory");
  let itemDescription = document.getElementById("itemDescription");
  let itemQuantity = document.getElementById("itemQuantity");
  let itemStore = document.getElementById("itemStore");
  let itemCost = document.getElementById("itemCost");
  let itemSelling = document.getElementById("itemSelling");
  let itemMFG = document.getElementById("itemMFG");
  let itemExpiry = document.getElementById("itemExpiry");
  

  let newRow = document.createElement("tr");
  newRow.innerHTML = `
        <td>${foodItemId}</td>
        <td>Image</td>
        <td>${itemName.value}</td>
        <td>${itemCategory.value}</td>
        <td>${itemDescription.value}</td>
        <td>${itemQuantity.value}</td>
        <td>${itemStore.value}</td>
        <td>${itemCost.value}</td>
        <td>${itemSelling.value}</td>
        <td>${itemMFG.value}</td>
        <td>${itemExpiry.value}</td>
        <td>
            <button class="update-btn"><i class="fas fa-edit"></i></button>
            <button class="delete-btn"><i class="fas fa-trash"></i></button>
        </td>
    `;



    let updateBtn = newRow.querySelector(".update-btn");
    updateBtn.addEventListener("click", function () {
        editFoodItem(this);
    });

    // ✅ Attach event listener to the "Delete" button
    let deleteBtn = newRow.querySelector(".delete-btn");
    deleteBtn.addEventListener("click", function () {
        deleteRow(this);
    });

  document.getElementById("foodTableBody").appendChild(newRow);
  foodItemId++;

  document.getElementById("foodItemForm").reset();
  closeForm();
}

function editFoodItem(button) {
  console.log("Edit button clicked!"); 
  let row = button.closest("tr");

  if (!row) {
      console.log("❌ Error: Could not find row!");
      return;
  }

  updateIndex = row; // Store row reference
  let cells = row.getElementsByTagName("td");

  console.log("Resetting form...");
  document.getElementById("foodItemForm").reset();

  document.getElementById("itemName").value = cells[2].textContent.trim();
  document.getElementById("itemCategory").value = cells[3].textContent.trim();
  document.getElementById("itemDescription").value = cells[4].textContent.trim();
  document.getElementById("itemQuantity").value = cells[5].textContent.trim();
  document.getElementById("itemStore").value = cells[6].textContent.trim();
  document.getElementById("itemCost").value = cells[7].textContent.trim();
  document.getElementById("itemSelling").value = cells[8].textContent.trim();
  document.getElementById("itemMFG").value = cells[9].textContent.trim();
  document.getElementById("itemExpiry").value = cells[10].textContent.trim();

  openForm(true);
}



function updateFoodItem(button) {
  if (!updateIndex) return;
  if (!validateForm()) return;

  let cells = updateIndex.getElementsByTagName("td");

  cells[2].textContent= document.getElementById("itemName").value.trim();
  cells[3].textContent= document.getElementById("itemCategory").value.trim();
  cells[4].textContent= document.getElementById("itemDescription").value.trim();
  cells[5].textContent= document.getElementById("itemQuantity").value.trim();
  cells[6].textContent= document.getElementById("itemStore").value.trim();
  cells[7].textContent= document.getElementById("itemCost").value.trim();
  cells[8].textContent= document.getElementById("itemSelling").value.trim();
  cells[9].textContent= document.getElementById("itemMFG").value.trim();
  cells[10].textContent= document.getElementById("itemExpiry").value.trim();

  updateIndex = null;
  document.getElementById("foodItemForm").reset();
  closeForm();
}

function deleteRow(button) {
  button.closest("tr").remove();
}


function validateForm() {
  let isValid = true;
  clearErrors();

  function showError(id, message) {
    document.getElementById(id).textContent = message;
  }

  let itemName = document.getElementById("itemName");
  let itemCategory = document.getElementById("itemCategory");
  let itemDescription = document.getElementById("itemDescription");
  let itemQuantity = document.getElementById("itemQuantity");
  let itemStore = document.getElementById("itemStore");
  let itemCost = document.getElementById("itemCost");
  let itemSelling = document.getElementById("itemSelling");
  let itemMFG = document.getElementById("itemMFG");
  let itemExpiry = document.getElementById("itemExpiry");

  if (!itemName.value.trim()) {
    showError("nameError", "Item name is required.");
    isValid = false;
  }
  if (!itemCategory.value.trim()) {
    showError("categoryError", "Category is required.");
    isValid = false;
  }
  if (!itemDescription.value.trim()) {
    showError("descriptionError", "Description is required.");
    isValid = false;
  }
  if (
    !itemQuantity.value.trim() ||
    isNaN(itemQuantity.value) ||
    itemQuantity.value <= 0
  ) {
    showError("quantityError", "Enter a valid quantity.");
    isValid = false;
  }
  if (!itemStore.value.trim()) {
    showError("storeError", "Store selection is required.");
    isValid = false;
  }
  if (!itemCost.value.trim() || isNaN(itemCost.value) || itemCost.value <= 0) {
    showError("costPriceError", "Enter a valid cost.");
    isValid = false;
  }
  if (
    !itemSelling.value.trim() ||
    isNaN(itemSelling.value) ||
    itemSelling.value <= 0
  ) {
    showError("sellingPriceError", "Enter a valid selling price.");
    isValid = false;
  }
  if (!itemMFG.value.trim()) {
    showError("MFG-Error", "Manufacturing date is required.");
    isValid = false;
  }
  if (!itemExpiry.value.trim()) {
    showError("expiryError", "Expiry date is required.");
    isValid = false;
  }

  console.log("Validation Result:", isValid);
  return isValid; // ✅ FIXED: Now returns true or false
}

function clearErrors() {
  let errorElements = document.querySelectorAll(".error-message");
  errorElements.forEach((element) => {
    element.textContent = "";
  });
}


function openForm() {
  document.getElementById("overlay").style.display = "block";
  document.getElementById("myForm").style.display = "block";
  document.body.classList.add("popup-open");

  // Fix the issue
  window.isUpdate = updateIndex !== null;

  if (!isUpdate) {
    document.getElementById("foodItemForm").reset();
    updateIndex = null;
  }
}


function closeForm() {
  document.getElementById("overlay").style.display = "none";
  document.getElementById("myForm").style.display = "none";
  document.body.classList.remove("popup-open");
  if (updateIndex !== null) {
    updateIndex = null; // Keep the row intact, just reset the reference
  } 
}

function populateStaticDropdowns() {
  let names = ["Pizza", "Burger", "Pasta"];
  let categories = ["Fast Food", "Beverages", "Desserts"];
  let stores = ["Store A", "Store B", "Store C"];

  let nameDropdown = document.getElementById("itemName");
  let categoryDropdown = document.getElementById("itemCategory");
  let storeDropdown = document.getElementById("itemStore");

  names.forEach((name) => {
    let option = document.createElement("option");
    option.value = name;
    option.textContent = name;
    nameDropdown.appendChild(option);
  });

  categories.forEach((category) => {
    let option = document.createElement("option");
    option.value = category;
    option.textContent = category;
    categoryDropdown.appendChild(option);
  });

  stores.forEach((store) => {
    let option = document.createElement("option");
    option.value = store;
    option.textContent = store;
    storeDropdown.appendChild(option);
  });
}
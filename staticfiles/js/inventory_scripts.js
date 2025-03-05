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

document.addEventListener("DOMContentLoaded", function () {
  document
    .getElementById("foodItemForm")
    .addEventListener("submit", function (event) {
      event.preventDefault();
      if (updateIndex !== null) {
        updateFoodItem();
      } else {
        addFoodItem();
      }
    });

  populateStaticDropdowns();
});

let foodItemId = 1;
let updateIndex = null;

function addFoodItem() {
  clearErrors();
  if (!validateForm()) return;

  let itemName = document.getElementById("itemName").value.trim();
  let itemCategory = document.getElementById("itemCategory").value.trim();
  let itemDescription = document.getElementById("itemDescription").value.trim();
  let itemQuantity = document.getElementById("itemQuantity").value.trim();
  let itemStore = document.getElementById("itemStore").value.trim();
  let itemCost = document.getElementById("itemCost").value.trim();
  let itemSelling = document.getElementById("itemSelling").value.trim();
  let itemMFG = document.getElementById("itemMFG").value.trim();
  let itemExpiry = document.getElementById("itemExpiry").value.trim();

  let foodTableBody = document.getElementById("foodTableBody");
  let newRow = document.createElement("tr");

  newRow.innerHTML = `
        <td>${foodItemId}</td>
        <td>Image</td>
        <td>${itemName}</td>
        <td>${itemCategory}</td>
        <td>${itemDescription}</td>
        <td>${itemQuantity}</td>
        <td>${itemStore}</td>
        <td>${itemCost}</td>
        <td>${itemSelling}</td>
        <td>${itemMFG}</td>
        <td>${itemExpiry}</td>
        <td>
            <button class="update-btn"><i class="fas fa-edit"></i></button>
            <button class="delete-btn"><i class="fas fa-trash"></i></button>
        </td>
    `;

  let updateBtn = newRow.querySelector(".update-btn");
  updateBtn.addEventListener("click", function () {
    editFoodItem(newRow);
  });

  let deleteBtn = newRow.querySelector(".delete-btn");
  deleteBtn.addEventListener("click", function () {
    deleteRow(newRow);
  });

  foodTableBody.appendChild(newRow);
  foodItemId++;
  document.getElementById("foodItemForm").reset();
  closeForm();
}

function editFoodItem(row) {
  console.log("Editing food item...");
  
  updateIndex = row; // Store row reference

  let cells = row.getElementsByTagName("td");

  document.getElementById("itemName").value = cells[2].textContent.trim();
  document.getElementById("itemCategory").value = cells[3].textContent.trim();
  document.getElementById("itemDescription").value = cells[4].textContent.trim();
  document.getElementById("itemQuantity").value = cells[5].textContent.trim();
  document.getElementById("itemStore").value = cells[6].textContent.trim();
  document.getElementById("itemCost").value = cells[7].textContent.trim();
  document.getElementById("itemSelling").value = cells[8].textContent.trim();
  document.getElementById("itemMFG").value = cells[9].textContent.trim();
  document.getElementById("itemExpiry").value = cells[10].textContent.trim();

  openForm();
}

function updateFoodItem() {
  if (!updateIndex) return;
  if (!validateForm()) return;

  let cells = updateIndex.getElementsByTagName("td");

  cells[2].textContent = document.getElementById("itemName").value.trim();
  cells[3].textContent = document.getElementById("itemCategory").value.trim();
  cells[4].textContent = document.getElementById("itemDescription").value.trim();
  cells[5].textContent = document.getElementById("itemQuantity").value.trim();
  cells[6].textContent = document.getElementById("itemStore").value.trim();
  cells[7].textContent = document.getElementById("itemCost").value.trim();
  cells[8].textContent = document.getElementById("itemSelling").value.trim();
  cells[9].textContent = document.getElementById("itemMFG").value.trim();
  cells[10].textContent = document.getElementById("itemExpiry").value.trim();

  updateIndex = null;
  document.getElementById("foodItemForm").reset();
  closeForm();
}

function deleteRow(row) {
  row.remove();
}

function openForm() {
  document.getElementById("overlay").style.display = "block";
  document.getElementById("myForm").style.display = "block";
  document.body.classList.add("popup-open");
}

function closeForm() {
  document.getElementById("overlay").style.display = "none";
  document.getElementById("myForm").style.display = "none";
  document.body.classList.remove("popup-open");
  updateIndex = null;
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

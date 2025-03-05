// Toggle search input on small devices
function toggleSearch() {
    let searchContainer = document.querySelector(".search-container");
    let searchInput = document.querySelector(".search-input");

    searchContainer.classList.toggle("active");
    if (searchContainer.classList.contains("active")) {
        searchInput.focus();
    }
}

// Search function
document.getElementById("searchInput").addEventListener("keyup", function () {
    let filter = this.value.toLowerCase();
    let rows = document.querySelectorAll("#supplierTableBody tr");

    rows.forEach(function (row) {
        let name = row.cells[1].textContent.toLowerCase();
        let company = row.cells[2].textContent.toLowerCase();

        if (name.includes(filter) || company.includes(filter)) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }
    });
});

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("supplierForm").addEventListener("submit", function (event) {
        event.preventDefault();
        if (updateIndex !== null) {
            updateSupplier();
        } else {
            addSupplier();
        }
    });

    populateStoreDropdown();
});

let supplierID = 1;
let updateIndex = null;

function addSupplier() {
    clearErrors();
    if (!validateForm()) return;

    let name = document.getElementById("supplierName").value.trim();
    let company = document.getElementById("companyName").value.trim();
    let email = document.getElementById("supplierEmail").value.trim();
    let address = document.getElementById("supplierAddress").value.trim();
    let phone = document.getElementById("supplierPhone").value.trim();
    let store = document.getElementById("supplierStore").value.trim();

    let tableBody = document.getElementById("supplierTableBody");
    let newRow = document.createElement("tr");
    newRow.innerHTML = `
        <td>${supplierID}</td>
        <td>${name}</td>
        <td>${company}</td>
        <td>${email}</td>
        <td>${address}</td>
        <td>${phone}</td>
        <td>${store}</td>
        <td>
            <button class="update-btn"><i class="fas fa-edit"></i></button>          
            <button class="delete-btn"><i class="fas fa-trash"></i></button>
        </td>
    `;

    // ✅ Attach event listener to the "Update" button after adding row
    let updateBtn = newRow.querySelector(".update-btn");
    updateBtn.addEventListener("click", function () {
        editSupplier(this);
    });

    // ✅ Attach event listener to the "Delete" button
    let deleteBtn = newRow.querySelector(".delete-btn");
    deleteBtn.addEventListener("click", function () {
        deleteSupplier(this);
    });

    tableBody.appendChild(newRow);
    supplierID++;
    document.getElementById("supplierForm").reset();
    closeForm();
}


function editSupplier(button) {
    console.log("Edit button clicked!"); // ✅ Check if function runs
    let row = button.closest("tr");

    if (!row) {
        console.log("❌ Error: Could not find row!");
        return;
    }

    console.log("Row found:", row); // ✅ Check row selection

    updateIndex = row;
    let cells = row.getElementsByTagName("td");

    console.log("Resetting form...");
    document.getElementById("supplierForm").reset();

    document.getElementById("supplierName").value = cells[1].textContent.trim();
    document.getElementById("companyName").value = cells[2].textContent.trim();
    document.getElementById("supplierEmail").value = cells[3].textContent.trim();
    document.getElementById("supplierAddress").value = cells[4].textContent.trim();
    document.getElementById("supplierPhone").value = cells[5].textContent.trim();
    document.getElementById("supplierStore").value = cells[6].textContent.trim();

    console.log("Form populated with row data.");
    openForm(true);
}




function updateSupplier() {
    if (!validateForm()) return;

    let cells = updateIndex.getElementsByTagName("td");
    cells[1].textContent = document.getElementById("supplierName").value.trim();
    cells[2].textContent = document.getElementById("companyName").value.trim();
    cells[3].textContent = document.getElementById("supplierEmail").value.trim();
    cells[4].textContent = document.getElementById("supplierAddress").value.trim();
    cells[5].textContent = document.getElementById("supplierPhone").value.trim();
    cells[6].textContent = document.getElementById("supplierStore").value.trim();

    updateIndex = null;
    document.getElementById("supplierForm").reset();
    closeForm();
}

function deleteSupplier(button) {
    button.closest("tr").remove();
}

function validateForm() {
    let isValid = true;
    clearErrors();

    function showError(input, message) {
        let errorSpan = document.getElementById(input.id + "Error");
        errorSpan.textContent = message;
        errorSpan.style.color = "red";
    }

    let name = document.getElementById("supplierName");
    let company = document.getElementById("companyName");
    let email = document.getElementById("supplierEmail");
    let address = document.getElementById("supplierAddress");
    let phone = document.getElementById("supplierPhone");
    let store = document.getElementById("supplierStore");

    if (!name.value.trim()) {
        showError(name, "Name is required");
        isValid = false;
    }
    if (!company.value.trim()) {
        showError(company, "Company Name is required");
        isValid = false;
    }
    if (!email.value.trim() || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
        showError(email, "Enter a valid email");
        isValid = false;
    }
    if (!address.value.trim()) {
        showError(address, "Address is required");
        isValid = false;
    }
    if (!phone.value.trim() || !/^[6789]\d{9}$/.test(phone.value)) {
        showError(phone, "Enter a valid 10-digit phone number starting with 6,7,8,9");
        isValid = false;
    }
    if (!store.value.trim()) {
        showError(store, "Please select a store");
        isValid = false;
    }
    return isValid;
}

function clearErrors() {
    let errorMessages = document.querySelectorAll(".error-message");
    errorMessages.forEach(error => error.textContent = "");
}

function openForm(isUpdate = false) {
    document.getElementById("overlay").style.display = "block";
    document.getElementById("myForm").style.display = "block";
    document.body.classList.add("popup-open");
    if (!isUpdate) {
        document.getElementById("supplierForm").reset();
        updateIndex = null;
    }
}

function closeForm() {
    document.getElementById("overlay").style.display = "none";
    document.getElementById("myForm").style.display = "none";
    document.body.classList.remove("popup-open");
    updateIndex = null;
}

function populateStoreDropdown() {
    let stores = ["Store A", "Store B", "Store C"];
    let dropdown = document.getElementById("supplierStore");
    stores.forEach(store => {
        let option = document.createElement("option");
        option.value = store;
        option.textContent = store;
        dropdown.appendChild(option);
    });
}

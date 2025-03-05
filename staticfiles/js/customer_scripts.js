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
  let rows = document.querySelectorAll("#customerBody tr");

  rows.forEach(function (row) {
    let store = row.cells[1].textContent.toLowerCase();
    let manager = row.cells[2].textContent.toLowerCase();

    if (store.includes(filter) || manager.includes(filter)) {
      row.style.display = "";
    } else {
      row.style.display = "none";
    }
  });
});

let ID = 1;
let updateIndex = null; // Customers the row reference for updating

document.addEventListener("DOMContentLoaded", function () {
  document
    .getElementById("customerForm")
    .addEventListener("submit", function (event) {
      event.preventDefault();
      if (validateForm()) {
        if (updateIndex !== null) {
          saveUpdatedCustomer(); // Update existing row
        } else {
          addCustomer(); // Add new row
        }
      }
    });
});

// Form validation function
function validateForm() {
  let email = document.getElementById("email");
  let phoneNo = document.getElementById("phoneNo");
  let gender = document.getElementById("gender");

  let emailValue = email.value.trim();
  let phoneNoValue = phoneNo.value.trim();
  let genderValue = gender.value.trim();

  // Regular expressions for validation
  let emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; // Valid email format
  let phoneNoRegex = /^(?:\+91[-\s]?)?[6-9]\d{9}$/;

  clearErrors();
  let isValid = true;

  // Email Validation
  if (!emailRegex.test(emailValue)) {
    showError(email, "Enter a valid email (e.g., user@example.com)");
    isValid = false;
  }
  // Password Validation
  if (!phoneNoRegex.test(phoneNoValue)) {
    showError(
      phoneNo,
      "Invalid Phone Format.Phone number must be 10 digits & start with 6-9 (e.g., 9876543210)"
    );
    isValid = false;
  }
  if (!genderValue) {
    showError(gender, "Gender selection is required.");
    isValid = false;
  }
  return isValid;
}

// Function to show error messages below the input field
function showError(input, message) {
  let errorSpan = document.createElement("span");
  errorSpan.classList.add("error-message");
  errorSpan.style.color = "red";
  errorSpan.style.fontSize = "12px";
  errorSpan.innerText = message;
  input.parentNode.appendChild(errorSpan);
}

// Function to add a new customer
function addCustomer() {
  if (!validateForm()) {
    return; // STOP adding data if validation fails
  }

  let firstName = document.getElementById("firstName").value.trim();
  let lastName = document.getElementById("lastName").value.trim();
  let address = document.getElementById("address").value.trim();
  let phoneNo = document.getElementById("phoneNo").value.trim();
  let email = document.getElementById("email").value.trim();
  let gender = document.getElementById("gender").value;

  let newRow = document.createElement("tr");
  newRow.innerHTML = `
        <td>${ID}</td>
        <td>${firstName}</td>
        <td>${lastName}</td>
        <td>${address}</td>
        <td>${phoneNo}</td>
        <td>${email}</td>
        <td>${gender}</td>
        <td class="action-buttons">
            <button class="update-btn" onclick="updateRow(this)"><i class="fas fa-edit"></i></button>
            <button class="delete-btn" onclick="deleteRow(this)"><i class="fas fa-trash"></i></button>
        </td>
    `;

  document.getElementById("customerBody").appendChild(newRow);
  ID++; // Increment ID
  document.getElementById("customerForm").reset();
  closeForm();
}

// Function to update a row
function updateRow(button) {
  let row = button.closest("tr");
  let columns = row.getElementsByTagName("td");

  document.getElementById("firstName").value = columns[1].textContent;
  document.getElementById("lastName").value = columns[2].textContent;
  document.getElementById("address").value = columns[3].textContent;
  document.getElementById("phoneNo").value = columns[4].textContent;
  document.getElementById("email").value = columns[5].textContent;
  document.getElementById("gender").value = columns[6].textContent;

  updateIndex = row; // Customer reference to the row for updating
  openForm(true);
}

// Function to save the updated customer details
function saveUpdatedCustomer() {
  if (updateIndex) {
    let firstName = document.getElementById("firstName").value.trim();
    let lastName = document.getElementById("lastName").value.trim();
    let address = document.getElementById("address").value.trim();
    let phoneNo = document.getElementById("phoneNo").value.trim();
    let email = document.getElementById("email").value.trim();
    let gender = document.getElementById("gender").value;

    updateIndex.cells[1].textContent = firstName;
    updateIndex.cells[2].textContent = lastName;
    updateIndex.cells[3].textContent = address;
    updateIndex.cells[4].textContent = phoneNo;
    updateIndex.cells[5].textContent = email;
    updateIndex.cells[6].textContent = gender;

    updateIndex = null; // Reset after update
    document.getElementById("customerForm").reset();
    closeForm();
  }
}

// Function to delete a row
function deleteRow(button) {
  button.closest("tr").remove();
}

// Open form modal
function openForm(isUpdate = false) {
  document.getElementById("overlay").style.display = "block";
  document.getElementById("myForm").style.display = "block";
  document.body.classList.add("popup-open");

  if (!isUpdate) {
    resetForm(); // Clears the form when adding a new customer
    updateIndex = null; // Clear any previous update reference
  }
}

// Close form modal
function closeForm() {
  document.getElementById("overlay").style.display = "none";
  document.getElementById("myForm").style.display = "none";
  document.body.classList.remove("popup-open");

  resetForm(); // Ensure form resets when closing
  updateIndex = null; // Reset update index when closing
}

// Function to reset the form
function resetForm() {
  document.getElementById("customerForm").reset();
}

// Function to clear all error messages
function clearErrors() {
  document.querySelectorAll(".error-message").forEach((el) => {
    el.textContent = "";
  });
}

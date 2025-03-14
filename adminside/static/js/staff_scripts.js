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
  let rows = document.querySelectorAll("#staffBody tr");

  rows.forEach(function (row) {
    let fullName = row.cells[1].textContent.toLowerCase();
    let userName = row.cells[2].textContent.toLowerCase();

    if (fullName.includes(filter) || userName.includes(filter)) {
      row.style.display = "";
    } else {
      row.style.display = "none";
    }
  });
});

let isUpdate = false; // Default: Adding new staff
let editingStaffId = null; // To store staff_id when updating

function openForm(update = false, staffData = null) {
  isUpdate = update; // Set mode (true for update, false for add)

  // Reset form
  document.getElementById("staffForm").reset();

  if (isUpdate && staffData) {
    // Fill form with existing staff data for update
    document.getElementById("userName").value = staffData.username;
    document.getElementById("fullName").value = staffData.fullname;
    document.getElementById("email").value = staffData.email;
    document.getElementById("password").value = staffData.password;
    document.getElementById("phoneNo").value = staffData.phone;
    document.getElementById("staffRole").value = staffData.role;
    document.getElementById("branches").value = staffData.branch;

    editingStaffId = staffData.id; // Store staff ID for update
  } else {
    editingStaffId = null; // Reset ID for adding new staff
  }

  document.getElementById("myForm").style.display = "block";
}

function validateForm() {
  let userName = document.getElementById("userName");
  let fullName = document.getElementById("fullName");
  let email = document.getElementById("email");
  let password = document.getElementById("password");
  let phoneNo = document.getElementById("phoneNo");
  let staffRole = document.getElementById("staffRole");
  let branches = document.getElementById("branches");

  if (
    !userName ||
    !fullName ||
    !email ||
    !password ||
    !phoneNo ||
    !staffRole ||
    !branches
  ) {
    console.error("One or more form fields are missing!");
    return false;
  }

  if (
    userName.value.trim() === "" ||
    fullName.value.trim() === "" ||
    email.value.trim() === "" ||
    password.value.trim() === "" ||
    phoneNo.value.trim() === "" ||
    staffRole.value.trim() === "" ||
    branches.value.trim() === ""
  ) {
    alert("All fields are required!");
    return false;
  }

  return true;
}

// let ID = 1;
// let updateIndex = null; // Customers the row reference for updating

// document.addEventListener("DOMContentLoaded", function () {
//   document
//     .getElementById("staffForm")
//     .addEventListener("submit", function (event) {
//       event.preventDefault();
//       if (validateForm()) {
//         if (updateIndex !== null) {
//           saveUpdatedStaff(); // Update existing row
//         } else {
//           addStaff(); // Add new row
//         }
//       }
//     });
// });

// // Form validation function
// function validateForm() {
//   let email = document.getElementById("email");
//   let password = document.getElementById("password");
//   let staffRole = document.getElementById("staffRole");
//   let branch = document.getElementById("branches");

//   let emailValue = email.value.trim();
//   let passwordValue = password.value.trim();
//   let staffRoleValue = staffRole.value.trim();
//   let branchValue = branch.value.trim();

//   // Regular expressions for validation
//   let emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; // Valid email format
//   let passwordRegex =
//     /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/; // Min 8 chars, 1 special character & 1 uppercase , 1 lowercase ,1 number

//   // Remove previous error messages
//   clearErrors();
//   let isValid = true;

//   // Email Validation
//   if (!emailRegex.test(emailValue)) {
//     showError(email, "Enter a valid email (e.g., user@example.com)");
//     isValid = false;
//   }

//   // Password Validation
//   if (!passwordRegex.test(passwordValue)) {
//     showError(
//       password,
//       "Password must be at least 8 characters, with at least 1 Uppercase, 1 lowercase , 1 special character and 1 number."
//     );
//     isValid = false;
//   }

//   if (!staffRoleValue) {
//     showError(staffRole, "Staff selection is required.");
//     isValid = false;
//   }

//   if (!branchValue) {
//     showError(branch, "Branch selection is required.");
//     isValid = false;
//   }

//   return isValid;
// }

// // Function to display error messages
// function showError(input, message) {
//   let errorSpan = document.createElement("span");
//   errorSpan.classList.add("error-message");
//   errorSpan.style.color = "red";
//   errorSpan.style.fontSize = "12px";
//   errorSpan.innerText = message;
//   input.parentNode.appendChild(errorSpan);
// }

// function addStaff() {
//   if (!validateForm()) {
//     return; // STOP adding data if validation fails
//   }

//   const defaultImageUrl = document
//     .getElementById("defaultImagePath")
//     .getAttribute("data-path");

//   let fullName = document.getElementById("fullName").value;
//   let userName = document.getElementById("userName").value;
//   let email = document.getElementById("email").value;
//   let password = document.getElementById("password").value;
//   let staffRole = document.getElementById("staffRole").value;
//   let branch = document.getElementById("branches").value;
//   let staffImageInput = document.getElementById("staffImage");

//   let staffImage =
//     staffImageInput.files.length > 0 ? staffImageInput.files[0] : null;

//   let imageUrl = staffImage ? URL.createObjectURL(staffImage) : defaultImageUrl;

//   let newRow = document.createElement("tr");
//   newRow.innerHTML = `
//         <td>${ID}</td>
//         <td><img src="${imageUrl}" class="food-img" width="50"></td>
//         <td>${fullName}</td>
//         <td>${userName}</td>
//         <td>${email}</td>
//         <td>${password}</td>
//         <td>${phoneNo}</td>
//         <td>${staffRole}</td>
//         <td>${branch}</td>
//         <td class="action-buttons">
//             <button class="update-btn" onclick="updateRow(this)"><i class="fas fa-edit"></i></button>
//             <button class="delete-btn" onclick="deleteRow(this)"><i class="fas fa-trash"></i></button>
//         </td>
//     `;
//   document.getElementById("staffBody").appendChild(newRow);
//   ID++; // Increment ID
//   document.getElementById("staffForm").reset();
//   closeForm();
// }

// // Function to update a row
// function updateRow(button) {
//   let row = button.closest("tr");
//   let columns = row.getElementsByTagName("td");

//   document.getElementById("fullName").value = columns[2].innerText;
//   document.getElementById("userName").value = columns[3].innerText;
//   document.getElementById("email").value = columns[4].innerText;
//   document.getElementById("password").value = columns[5].innerText;
//   document.getElementById("phoneNo").value = columns[6].innerText;
//   document.getElementById("staffRole").value = columns[7].innerText;
//   document.getElementById("branches").value = columns[8].innerText;

//   let image = document.getElementById("staffImage");
//   if (image) {
//     image.src = columns[1].querySelector("img").src;
//   }

//   updateIndex = row; // Staff reference to the row for updating
//   openForm(true);
// }

// // Function to save the updated customer details
// function saveUpdatedStaff() {
//   if (updateIndex) {
//     const defaultImageUrl = document
//       .getElementById("defaultImagePath")
//       .getAttribute("data-path");

//     let fullName = document.getElementById("fullName").value.trim();
//     let userName = document.getElementById("userName").value.trim();
//     let email = document.getElementById("email").value.trim();
//     let password = document.getElementById("password").value.trim();
//     let staffRole = document.getElementById("staffRole").value.trim();
//     let branch = document.getElementById("branches").value.trim();
//     let staffImageInput = document.getElementById("staffImage");

//     let staffImage =
//       staffImageInput.files.length > 0 ? staffImageInput.files[0] : null;

//     let imageUrl = staffImage
//       ? URL.createObjectURL(staffImage)
//       : defaultImageUrl;

//     updateIndex.cells[1].innerHTML = `<img src="${imageUrl}" class="food-img" width="50">`;
//     updateIndex.cells[2].textContent = fullName;
//     updateIndex.cells[3].textContent = userName;
//     updateIndex.cells[4].textContent = email;
//     updateIndex.cells[5].textContent = password;
//     updateIndex.cells[6].textContent = staffRole;
//     updateIndex.cells[7].textContent = branch;

//     updateIndex = null; // Reset after update
//     document.getElementById("staffForm").reset();
//     closeForm();
//   }
// }

// // Function to delete a row
// function deleteRow(button) {
//   button.closest("tr").remove();
// }

// // Open form modal
// function openForm() {
//   document.getElementById("overlay").style.display = "block";
//   document.getElementById("myForm").style.display = "block";
//   document.body.classList.add("popup-open");

//   if (!isUpdate) {
//     resetForm(); // Clears the form when adding a new staff
//     updateIndex = null; // Clear any previous update reference
//   }
// }

// // Close form modal
// function closeForm() {
//   document.getElementById("overlay").style.display = "none";
//   document.getElementById("myForm").style.display = "none";
//   document.body.classList.remove("popup-open");

//   resetForm(); // Ensure form resets when closing
//   updateIndex = null; // Reset update index when closing
// }

// // Function to reset the form
// function resetForm() {
//   document.getElementById("staffForm").reset();
// }

// // Function to clear all error messages
// function clearErrors() {
//   document.querySelectorAll(".error-message").forEach((el) => {
//     el.textContent = "";
//   });
// }

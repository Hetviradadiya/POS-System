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
  let rows = document.querySelectorAll("#staffTableBody tr");
  let matchFound = false;

  rows.forEach(function (row) {
    if (row.id === "noDataRow") return;

    let fullname = row.cells[2].textContent.toLowerCase();
    let username = row.cells[3].textContent.toLowerCase();

    if (fullname.includes(filter) || username.includes(filter)) {
      row.style.display = "";
      matchFound = true;
    } else {
      row.style.display = "none";
    }
  });

  let tableBody = document.getElementById("staffTableBody");
  let noData = document.getElementById("noDataRow");

  if (filter && !matchFound) {
    if (!noData) {
      noData = document.createElement("tr");
      noData.id = "noDataRow";
      noData.innerHTML = `<td colspan="10" style="text-align: center;">No data found</td>`; //add no datafound row
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
    document.querySelector(".form-container h1").innerText = "Add Staff";
    document.querySelector(".form-buttons button[type='submit']").innerText =
      "Add Staff";
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
  document.getElementById("staffId").value = "";
  document.getElementById("staffUserName").value = "";
  document.getElementById("staffFullName").value = "";
  document.getElementById("staffImage").value = "";
  document.getElementById("staffPhoneNo").value = "";
  document.getElementById("staffEmail").value = "";
  document.getElementById("staffPassword").value = "";
  document.getElementById("staffRole").value = "";
  document.getElementById("branch").value = "";
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

function editstaff(
  staff_id,
  staff_img,
  staff_username,
  staff_fullname,
  staff_email,
  staff_password,
  staff_phone_no,
  staff_role,
  branch
) {
  document.getElementById("staffId").value = staff_id;
  if (staff_img) {
    document.getElementById("staffImage").src = staff_img;
  } else {
    document.getElementById("staffImage").src =
      "/staff_images/default-profile.jpg"; // Default image
  }
  document.getElementById("staffUserName").value = staff_username;
  document.getElementById("staffFullName").value = staff_fullname;
  document.getElementById("staffEmail").value = staff_email;
  document.getElementById("staffPassword").value = staff_password;
  document.getElementById("staffPhoneNo").value = staff_phone_no;
  document.getElementById("staffRole").value = staff_role;
  // document.getElementById("branch").value = branch;

  let branchId = extractId(branch);
  let branchSelect = document.getElementById("branch");
  for (let option of branchSelect.options) {
    if (option.value == branchId) {
      option.selected = true;
      break;
    }
  }
  document.querySelector(".form-container h1").innerText = "Update Staff";
  document.querySelector(".form-buttons button[type='submit']").innerText =
    "Update Staff";

  openForm(true); // Open form for update
}

//form validation
document
  .getElementById("staffForm")
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

    const staffUserName = document.getElementById("staffUserName").value.trim();
    if (!staffUserName) {
      event.preventDefault();
      showError("staffUserName", "staff UserName is required!");
      isValid = false;
    }

    const staffFullName = document.getElementById("staffFullName").value;
    if (!staffFullName) {
      showError("staffFullName", "staff FullName is required!");
      isValid = false;
    }

    const staffEmail = document.getElementById("staffEmail").value.trim();
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

    if (!staffEmail) {
      event.preventDefault();
      showError("staffEmail", "Staff Email is required!");
      isValid = false;
    } else if (!emailPattern.test(staffEmail)) {
      event.preventDefault();
      showError("staffEmail", "Enter a valid email address!");
      isValid = false;
    }

    const staffPassword = document.getElementById("staffPassword").value;
    if (!staffPassword) {
      showError("staffPassword", "staff Password is required!");
      isValid = false;
    }

    const staffPhoneNo = document.getElementById("staffPhoneNo").value.trim();
    const phoneRegex =
      /^\+(1\d{10}|91\d{10}|44\d{9,10}|81\d{9,11}|49\d{10,11}|33\d{9}|61\d{9}|86\d{10,11})$/;

    if (!staffPhoneNo) {
      event.preventDefault();
      showError("staffPhoneNo", "Staff PhoneNo is required!.");
    } else if (!phoneRegex.test(staffPhoneNo)) {
      event.preventDefault();
      showError(
        "staffPhoneNo",
        "Enter a valid phone number (e.g., +919876543210)."
      );
      isValid = false;
    }

    const staffRole = document.getElementById("staffRole").value;
    if (!staffRole) {
      showError("staffRole", "staff Role is required!");
      isValid = false;
    }

    const branch = document.getElementById("branch").value;
    if (!branch) {
      showError("branch", "branch is required!");
      isValid = false;
    }

    if (!isValid) {
      event.preventDefault(); // Prevent form submission if validation fails
      document.getElementById("overlay").style.display = "block"; // Keep the form open
      document.getElementById("myForm").style.display = "block";
    }
  });

function previewImage(event) {
  let reader = new FileReader();
  reader.onload = function () {
    document.getElementById("staffImagePreview").src = reader.result;
  };
  reader.readAsDataURL(event.target.files[0]);
}


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

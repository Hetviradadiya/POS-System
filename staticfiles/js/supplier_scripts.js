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
  let rows = document.querySelectorAll("#supplierTableBody tr");
  let matchFound = false;

  rows.forEach(function (row) {
    if (row.id === "noDataRow") return;

    let name = row.cells[1].textContent.toLowerCase();
    let company = row.cells[4].textContent.toLowerCase();

    if (name.includes(filter) || company.includes(filter)) {
      row.style.display = "";
      matchFound = true;
    } else {
      row.style.display = "none";
    }
  });

  let tableBody = document.getElementById("supplierTableBody");
  let noData = document.getElementById("noDataRow");

  if (filter && !matchFound) {
    if (!noData) {
      noData = document.createElement("tr");
      noData.id = "noDataRow";
      noData.innerHTML = `<td colspan="8" style="text-align: center;">No data found</td>`; //add no datafound row
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
    document.querySelector(".form-container h1").innerText = "Add Supplier";
    document.querySelector(".form-buttons button[type='submit']").innerText =
      "Add Supplier";
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
  document.getElementById("supplierId").value = "";
  document.getElementById("supplierName").value = "";
  document.getElementById("supplierEmail").value = "";
  document.getElementById("supplierPhoneNo").value = "";
  document.getElementById("companyName").value = "";
  document.getElementById("supplierAddress").value = "";
}

//Clear validation errors
function clearErrors() {
  document
    .querySelectorAll(".error")
    .forEach((el) => el.classList.remove("error"));
  document.querySelectorAll(".error-message").forEach((el) => el.remove()); // Remove error messages
}

function editsupplier(
  supplier_id,
  supplier_name,
  supplier_email,
  supplier_phone_no,
  company_name,
  address
) {
  document.getElementById("supplierId").value = supplier_id;
  document.getElementById("supplierName").value = supplier_name;
  document.getElementById("supplierEmail").value = supplier_email;
  document.getElementById("supplierPhoneNo").value = supplier_phone_no;
  document.getElementById("companyName").value = company_name;
  document.getElementById("supplierAddress").value = address;

  document.querySelector(".form-container h1").innerText = "Update Supplier";
  document.querySelector(".form-buttons button[type='submit']").innerText =
    "Update Supplier";

  openForm(true); // Open form for update
}

//form validation
document
  .getElementById("supplierForm")
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

    const supplierName = document.getElementById("supplierName").value.trim();
    if (!supplierName) {
      showError("supplierName", "Supplier name is required!");
      isValid = false;
    }

    const supplierEmail = document.getElementById("supplierEmail").value.trim();
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

    if (!supplierEmail) {
      showError("supplierEmail", "Supplier Email is required!");
      isValid = false;
    } else if (!emailPattern.test(supplierEmail)) {
      showError("supplierEmail", "Enter a valid email address!");
      isValid = false;
    }

    const supplierPhoneNo = document
      .getElementById("supplierPhoneNo")
      .value.trim();
    const phoneRegex =
      /^\+(1\d{10}|91\d{10}|44\d{9,10}|81\d{9,11}|49\d{10,11}|33\d{9}|61\d{9}|86\d{10,11})$/;

    if (!supplierPhoneNo) {
      showError("supplierPhoneNo", "Supplier PhoneNo is required!.");
    } else if (!phoneRegex.test(supplierPhoneNo)) {
      showError(
        "supplierPhoneNo",
        "Enter a valid phone number (e.g., +919876543210)."
      );
      isValid = false;
    }

    const companyName = document.getElementById("companyName").value;
    if (!companyName) {
      showError("companyName", "company Name is required!");
      isValid = false;
    }
    const supplierAddress = document.getElementById("supplierAddress").value;
    if (!supplierAddress) {
      showError("supplierAddress", "supplier Address is required!");
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

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
  let rows = document.querySelectorAll("#branchTableBody tr");
  let matchFound = false;

  rows.forEach(function (row) {
    if (row.id === "noDataRow") return;

    let branch = row.cells[1].textContent.toLowerCase();
    let area = row.cells[3].textContent.toLowerCase();

    if (branch.includes(filter) || area.includes(filter)) {
      row.style.display = "";
      matchFound = true;
    } else {
      row.style.display = "none";
    }
  });

  let tableBody = document.getElementById("branchTableBody");
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
    document.querySelector(".form-container h1").innerText = "Add Branch";
    document.querySelector(".form-buttons button[type='submit']").innerText =
      "Add Branch";
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
  document.getElementById("branchId").value = "";
  document.getElementById("branchName").value = "";
  document.getElementById("manager").value = "";
  document.getElementById("branchArea").value = "";
  document.getElementById("branchLocation").value = "";
  document.getElementById("phoneNo").value = "";
  document.getElementById("branchStatus").value = "";
}

//Clear validation errors
function clearErrors() {
  document
    .querySelectorAll(".error")
    .forEach((el) => el.classList.remove("error"));
  document.querySelectorAll(".error-message").forEach((el) => el.remove()); // Remove error messages
}

function editBranch(
  branchId,
  branchName,
  branchLocation,
  branchArea,
  phoneNo,
  branchStatus,
  manager
) {
  document.getElementById("branchId").value = branchId;
  document.getElementById("branchName").value = branchName;
  document.getElementById("manager").value = manager || "";
  document.getElementById("branchArea").value = branchArea;
  document.getElementById("branchLocation").value = branchLocation;
  document.getElementById("phoneNo").value = phoneNo;

  let statusSelect = document.getElementById("branchStatus");
  if (branchStatus === "Active" || branchStatus === "Inactive") {
    statusSelect.value = branchStatus;
  } else {
    statusSelect.value = "";
  }

  document.querySelector(".form-container h1").innerText = "Update Branch";
  document.querySelector(".form-buttons button[type='submit']").innerText =
    "Update Branch";

  openForm(true); // Open form for update
}

//form validation
document
  .getElementById("branchForm")
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

    const branchName = document.getElementById("branchName").value.trim();
    if (!branchName) {
      showError("branchName", "Branch name is required!");
      isValid = false;
    }

    const branchLocation = document
      .getElementById("branchLocation")
      .value.trim();
    if (!branchLocation) {
      showError("branchLocation", "Branch location is required!");
      isValid = false;
    }

    const branchArea = document.getElementById("branchArea").value.trim();
    if (!branchArea) {
      showError("branchArea", "Branch area is required!");
      isValid = false;
    }

    const phoneNo = document.getElementById("phoneNo").value.trim();
    const phoneRegex =
      /^\+(1\d{10}|91\d{10}|44\d{9,10}|81\d{9,11}|49\d{10,11}|33\d{9}|61\d{9}|86\d{10,11})$/;

    if (!phoneRegex.test(phoneNo)) {
      showError("phoneNo", "Enter a valid phone number (e.g., +919876543210).");
      isValid = false;
    }

    const branchStatus = document.getElementById("branchStatus").value;
    if (!branchStatus) {
      showError("branchStatus", "Branch status is required!");
      isValid = false;
    }

    if (!isValid) {
      event.preventDefault(); // Prevent form submission if validation fails
      document.getElementById("overlay").style.display = "block"; // Keep the form open
      document.getElementById("myForm").style.display = "block";
    }
  });

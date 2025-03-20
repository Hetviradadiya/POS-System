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
  let rows = document.querySelectorAll("#categoryBody tr");
  let matchFound = false;

  rows.forEach(function (row) {
    if (row.id === "noDataRow") return;

    let name = row.cells[1].textContent.toLowerCase();

    if (name.includes(filter)) {
      row.style.display = "";
      matchFound = true;
    } else {
      row.style.display = "none";
    }
  });

  let tableBody = document.getElementById("categoryBody");
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

//open form
function openForm(isUpdate = false) {
  document.getElementById("overlay").style.display = "block";
  document.getElementById("myForm").style.display = "block";
  document.body.classList.add("popup-open");

  if (!isUpdate) {
    resetForm(); // Clears the form
    document.querySelector(".form-container h1").innerText = "Add Category";
    document.querySelector(".form-buttons button[type='submit']").innerText =
      "Add Category";
  }
}

// Close form
function closeForm() {
  document.getElementById("overlay").style.display = "none";
  document.getElementById("myForm").style.display = "none";
  document.body.classList.remove("popup-open");

  resetForm(); //  form resets
  clearErrors();
}

//reset form
function resetForm() {
  document.getElementById("categoryForm").reset(); // Resets all input fields
}

//Clear validation errors
function clearErrors() {
  document
    .querySelectorAll(".error")
    .forEach((el) => el.classList.remove("error"));
  document.querySelectorAll(".error-message").forEach((el) => el.remove()); // Remove error messages
}

function editCategory(categoryId, categoryName, categoryStatus) {
  document.getElementById("categoryId").value = categoryId;
  document.getElementById("categoryName").value = categoryName;
  document.getElementById("categoryStatus").checked = categoryStatus === "True";


  document.querySelector(".form-container h1").innerText = "Update Category";
  document.querySelector(".form-buttons button[type='submit']").innerText =
    "Update Category";
  openForm(true); // Open form
}

document
  .getElementById("categoryForm")
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

    const categoryName = document.getElementById("categoryName").value.trim();
    if (!categoryName) {
      showError("categoryName", "Category Name is required!");
      isValid = false;
    }

    if (!isValid) {
      event.preventDefault(); // Prevent form submission if validation fails
      document.getElementById("overlay").style.display = "block"; // Keep the form open
      document.getElementById("myForm").style.display = "block";
    }
  });



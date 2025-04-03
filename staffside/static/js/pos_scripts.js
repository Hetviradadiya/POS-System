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
  // console.log("Search filter:", filter);

  let productCards = document.querySelectorAll("#product-container .col-md-6");
  // console.log("Total product cards found:", productCards.length);

  let matchFound = false;

  productCards.forEach(function (card, index) {
    let foodItemElement = card.querySelector(".card-body .card-title");
    let foodItemName = foodItemElement
      ? foodItemElement.textContent.toLowerCase().trim()
      : "";

    // console.log(`Card ${index + 1}:`, foodItemName);

    if (!foodItemName) {
      card.style.setProperty("display", "none", "important");
      return;
    }

    if (foodItemName.includes(filter)) {
      card.style.setProperty("display", "block", "important"); // ✅ Force show
      matchFound = true;
    } else {
      card.style.setProperty("display", "none", "important"); // ✅ Force hide
    }

    // console.log(
    //   `Card ${index + 1} display style:`,
    //   getComputedStyle(card).display
    // );
  });

  // Handle "No matching food item found"
  let productContainer = document.getElementById("product-container");
  let noData = document.getElementById("noDataRow");

  if (filter && !matchFound) {
    if (!noData) {
      noData = document.createElement("div");
      noData.id = "noDataRow";
      noData.innerHTML = `<p style="text-align: center;">No matching food item found</p>`;
      productContainer.appendChild(noData);
    }
  } else {
    if (noData) {
      noData.remove();
    }
  }

  // Reset when search is cleared
  if (filter === "") {
    productCards.forEach((card) => {
      card.style.setProperty("display", "block", "important"); // ✅ Reset visibility
    });
    if (noData) noData.remove();
  }
});







// Store and restore table selection
document.addEventListener("DOMContentLoaded", function () {
  const tableSelector = document.getElementById("table-selector");

  // Restore selected table from session (handled via URL param)
  if (tableSelector) {
    const urlParams = new URLSearchParams(window.location.search);
    const savedTable = urlParams.get("table_id");

    if (savedTable) {
      const optionExists = [...tableSelector.options].some(
        (opt) => opt.value === savedTable
      );
      if (optionExists) {
        tableSelector.value = savedTable;
      }
    }

    // Reload page when table changes
    tableSelector.addEventListener("change", function () {
      const selectedTable = this.value;
      window.location.href = `?table_id=${selectedTable}`;
    });
  }

  // Add to Cart buttons
  document.querySelectorAll(".add-to-cart-button").forEach((button) => {
    button.addEventListener("click", function (event) {
      let productId = this.getAttribute("data-product-id");
      if (!productId) {
        console.error("Product ID not found in button dataset.");
        return;
      }
      validateCart(event, productId);
    });
  });
});

// Define selectSize in global scope
function selectSize(event, productId, size) {
  event.preventDefault(); // Prevent default behavior if event exists

  let sizeInput = document.getElementById(`size-${productId}`);
  if (!sizeInput) {
    console.error(`Size input not found for product ID: ${productId}`);
    return;
  }

  sizeInput.value = size;

  // Highlight selected size button
  document
    .querySelectorAll(`[data-product="${productId}"]`)
    .forEach((btn) => btn.classList.remove("active-size"));

  event.target.classList.add("active-size");
}

// validateCart in global scope
function validateCart(event, productId) {
  if (event) event.preventDefault(); // Ensure event is properly handled

  let tableSelector = document.getElementById("table-selector");
  let selectedTable = tableSelector ? tableSelector.value : null;
  let sizeInput = document.getElementById(`size-${productId}`);

  console.log("Selected Table ID:", selectedTable);
  console.log("Size Input Value:", sizeInput ? sizeInput.value : "Not Found");

  // if (!selectedTable) {
  //   alert("Please select a table first.");
  //   return false;
  // }

  // If no size is selected, auto-select "Medium"
  if (!sizeInput || !sizeInput.value) {
    let mediumSizeBtn = document.querySelector(
      `[data-product="${productId}"][data-size="Medium"]`
    );
    if (mediumSizeBtn) {
      sizeInput.value = "Medium"; // Set value to Medium
      mediumSizeBtn.classList.add("active-size"); // Highlight the button
      console.log(`Auto-selected Medium size for Product ID: ${productId}`);
    } else {
      alert("Please select a size.");
      return false;
    }
  }

  // Save table selection before form submission
  localStorage.setItem("selectedTable", selectedTable);

  // If all conditions are true, submit the form
  let form = document.getElementById(`add-to-cart-form-${productId}`);
  if (form) {
    let tableField = form.querySelector('input[name="table_id"]');
    let sizeField = form.querySelector('input[name="size"]');

    if (tableField) tableField.value = selectedTable; // table_id is set
    if (sizeField) sizeField.value = sizeInput.value; // size is set

    console.log("Submitting Form with Table ID:", tableField.value);
    console.log("Submitting Form with Size:", sizeField.value);

    form.submit();
  } else {
    console.error(`Form not found for product ID: ${productId}`);
  }

  return true;
}

function updateQuantity(cartId, tableId, change) {
  let quantityElement = document.getElementById(`quantity-${cartId}`);
  let currentQuantity = parseInt(quantityElement.innerText);
  let newQuantity = currentQuantity + change;

  if (newQuantity < 1) {
    return; // Prevent quantity from going below 1
  }

  // Create a form dynamically
  let form = document.createElement("form");
  form.method = "POST";
  form.action = window.location.href; // Submits to the same page

  // CSRF Token (required for Django)
  let csrfToken = document.querySelector(
    "input[name='csrfmiddlewaretoken']"
  ).value;
  let csrfInput = document.createElement("input");
  csrfInput.type = "hidden";
  csrfInput.name = "csrfmiddlewaretoken";
  csrfInput.value = csrfToken;
  form.appendChild(csrfInput);

  // Hidden inputs to send cart_id, table_id, and quantity change
  let actionInput = document.createElement("input");
  actionInput.type = "hidden";
  actionInput.name = "action";
  actionInput.value = "update_quantity";
  form.appendChild(actionInput);

  let cartInput = document.createElement("input");
  cartInput.type = "hidden";
  cartInput.name = "cart_id";
  cartInput.value = cartId;
  form.appendChild(cartInput);

  let tableInput = document.createElement("input");
  tableInput.type = "hidden";
  tableInput.name = "table_id";
  tableInput.value = tableId;
  form.appendChild(tableInput);

  let changeInput = document.createElement("input");
  changeInput.type = "hidden";
  changeInput.name = "change";
  changeInput.value = change;
  form.appendChild(changeInput);

  document.body.appendChild(form);
  form.submit(); // Submit the form to update quantity in Django
}

document.addEventListener("DOMContentLoaded", function () {
  let cartItemsCount = document.getElementById("cart-items-count");
  let cartTotalPrice = document.getElementById("cart-total-price");

  // update quantity of already added cart
  function updateCartSummary(price) {
    let currentCount = parseInt(cartItemsCount.textContent);
    let currentTotal = parseFloat(cartTotalPrice.textContent.replace("₹", ""));

    cartItemsCount.textContent = currentCount + 1;
    cartTotalPrice.textContent = "₹" + (currentTotal + price).toFixed(2);
  }

  // Add-to-cart button
  document.querySelectorAll(".add-to-cart").forEach((button) => {
    button.addEventListener("click", function () {
      let price = parseFloat(this.getAttribute("data-price"));
      updateCartSummary(price);
    });
  });
});

document.addEventListener("DOMContentLoaded", function () {
  document
    .getElementById("place-order-form")
    .addEventListener("submit", function (event) {
      let tableId = document.getElementById("table_id").value;
      if (!tableId) {
        alert("Table is not selected!");
        event.preventDefault(); // Prevent form submission
      } else {
        console.log("Submitting order for table:", tableId);
      }
    });
});

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

  let productCards = document.querySelectorAll(
    "#product-container .product-col"
  );
  // console.log("Total product cards found:", productCards.length);

  let matchFound = false;

  productCards.forEach(function (card, index) {
    let foodItemElement = card.querySelector(".card-title");
    let foodItemName = foodItemElement
      ? foodItemElement.textContent.toLowerCase().trim()
      : "";

    // console.log(`Card ${index + 1}:`, foodItemName);

    if (!foodItemName) {
      card.style.setProperty("display", "none", "important");
      return;
    }

    if (foodItemName.includes(filter)) {
      card.style.setProperty("display", "flex", "important"); // Force show
      matchFound = true;
    } else {
      card.style.setProperty("display", "none", "important"); // Force hide
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
      card.style.setProperty("display", "flex", "important"); // Reset visibility
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

// validateCart in global scope
function validateCart(event, productId) {
  if (event) event.preventDefault();

  let tableSelector = document.getElementById("table-selector");
  let selectedTable = tableSelector ? tableSelector.value : null;
  let sizeInput = document.getElementById(`size-${productId}`);

  if (!selectedTable) {
    alert("Please select a table.");
    return false;
  }


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

 document
   .getElementById("customer-selector")
   .addEventListener("change", function () {
     const selectedCustomer = this.value;
     document.getElementById("customer_id_input").value = selectedCustomer;
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
// Define selectSize in global scope
function selectSize(event, productId, size) {
  event.preventDefault(); // Prevent default behavior if event exists

  let sizeInput = document.getElementById(`size-${productId}`);
  let priceInput = document.querySelector(
    `#add-to-cart-form-${productId} input[name="price"]`
  );
  let originalPrice = parseFloat(priceInput.dataset.originalPrice);

  if (!sizeInput || !priceInput) {
    console.error(`Required elements not found for product ID: ${productId}`);
    return;
  }

  // Update the size input value
  sizeInput.value = size;

  // Calculate new price based on size
  let newPrice;
  if (size === "Small") {
    newPrice = originalPrice * 0.8; // 20% less
  } else if (size === "Large") {
    newPrice = originalPrice * 1.2; // 20% more
  } else {
    newPrice = originalPrice; // Medium, same price
  }

  // Update price input field
  priceInput.value = newPrice.toFixed(2);

  // Highlight the selected size button
  document
    .querySelectorAll(`[data-product="${productId}"]`)
    .forEach((btn) => btn.classList.remove("active-size"));

  event.target.classList.add("active-size");

  console.log(`Selected Size: ${size}, Updated Price: ₹${newPrice.toFixed(2)}`);
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

function setOrderType(type) {
  const tableId = document.getElementById("table-selector").value || "null";
  localStorage.setItem(`order_type_table_${tableId}`, type);

  // Update hidden input in all add-to-cart forms
  document.querySelectorAll('input[name="order_type"]').forEach((input) => {
    input.value = type;
  });

  // Update place order form too
  const placeOrderFormOrderType = document.querySelector(
    "#place-order-form input[name='order_type']"
  );
  if (placeOrderFormOrderType) {
    placeOrderFormOrderType.value = type;
  }

  // Highlight selected button
  document.querySelectorAll(".order-type-button").forEach((btn) => {
    if (btn.value === type) {
      btn.classList.add("selected-order-type");
    } else {
      btn.classList.remove("selected-order-type");
    }
  });

  // Try to save customer if both values are now set
  trySaveOrderTypeAndCustomer(tableId);
}

// function trySaveOrderTypeAndCustomer(tableId) {
//   const customerSelector = document.getElementById("customer-selector");
//   const customerInput = document.getElementById("customer_id_input");

//   const currentOrderType = localStorage.getItem(`order_type_table_${tableId}`);
//   const currentCustomerId = customerSelector?.value;

//   // Save only when both values are selected and not already saved
//   if (
//     currentOrderType &&
//     currentCustomerId &&
//     !localStorage.getItem(`customer_table_${tableId}`)
//   ) {
//     localStorage.setItem(`customer_table_${tableId}`, currentCustomerId);

//     document.querySelectorAll("input[name='customer_id']").forEach((input) => {
//       input.value = currentCustomerId;
//     });

//     // Lock both
//     if (customerSelector) customerSelector.disabled = true;
//     document.querySelectorAll(".order-type-button").forEach((btn) => {
//       btn.disabled = true;
//     });
//   }
// }

function trySaveOrderTypeAndCustomer(tableId) {
  const customerSelector = document.getElementById("customer-selector");
  const customerInput = document.getElementById("customer_id_input");

  const currentOrderType = localStorage.getItem(`order_type_table_${tableId}`);
  const currentCustomerId = customerSelector?.value;

  if (currentOrderType && currentCustomerId) {
    localStorage.setItem(`customer_table_${tableId}`, currentCustomerId);

    document.querySelectorAll("input[name='customer_id']").forEach((input) => {
      input.value = currentCustomerId;
    });

    // Lock both
    if (customerSelector) customerSelector.disabled = true;
    document.querySelectorAll(".order-type-button").forEach((btn) => {
      btn.disabled = true;
    });
  }
}
document.getElementById("reset-table").addEventListener("click", function () {
  const tableId = document.getElementById("table-selector").value;
  localStorage.removeItem(`order_type_table_${tableId}`);
  localStorage.removeItem(`customer_table_${tableId}`);
  location.reload(); // or reapply logic to unlock UI
});

document.addEventListener("DOMContentLoaded", function () {
  const tableSelector = document.getElementById("table-selector");
  const customerSelector = document.getElementById("customer-selector");
  const customerInput = document.getElementById("customer_id_input");

  function applySavedOrderAndCustomer(tableId) {
    const savedOrderType = localStorage.getItem(`order_type_table_${tableId}`);
    const savedCustomer = localStorage.getItem(`customer_table_${tableId}`);

    if (savedOrderType) {
      // Highlight selected order type button
      document.querySelectorAll(".order-type-button").forEach((btn) => {
        btn.classList.toggle(
          "selected-order-type",
          btn.value === savedOrderType
        );
      });

      // Set hidden inputs
      document.querySelectorAll('input[name="order_type"]').forEach((input) => {
        input.value = savedOrderType;
      });

      const placeOrderFormOrderType = document.querySelector(
        "#place-order-form input[name='order_type']"
      );
      if (placeOrderFormOrderType) {
        placeOrderFormOrderType.value = savedOrderType;
      }
    }

    if (savedCustomer && customerSelector) {
      customerSelector.value = savedCustomer;

      // Update all customer_id inputs
      document
        .querySelectorAll("input[name='customer_id']")
        .forEach((input) => {
          input.value = savedCustomer;
        });
    }

    // Disable if both are set
    if (savedOrderType && savedCustomer) {
      if (customerSelector) customerSelector.disabled = true;
      document.querySelectorAll(".order-type-button").forEach((btn) => {
        btn.disabled = true;
      });
    } else {
      if (customerSelector) customerSelector.disabled = false;
      document.querySelectorAll(".order-type-button").forEach((btn) => {
        btn.disabled = false;
      });
    }
  }

  // On page load
  if (tableSelector && tableSelector.value) {
    applySavedOrderAndCustomer(tableSelector.value);
  }

  // Table change
  if (tableSelector) {
    tableSelector.addEventListener("change", function () {
      const selectedTable = this.value;
      applySavedOrderAndCustomer(selectedTable);
      window.location.href = `?table_id=${selectedTable}`;
    });
  }

  // Customer change
  if (customerSelector) {
    customerSelector.addEventListener("change", function () {
      const tableId = tableSelector?.value;
      if (tableId) trySaveOrderTypeAndCustomer(tableId);
    });
  }
});

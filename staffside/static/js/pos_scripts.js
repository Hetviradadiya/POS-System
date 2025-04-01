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

  // ✅ Restore selected table from session (handled via URL param)
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

    // ✅ Reload page when table changes
    tableSelector.addEventListener("change", function () {
      const selectedTable = this.value;
      window.location.href = `?table_id=${selectedTable}`;
    });
  }

  // ✅ Attach event listeners to Add to Cart buttons
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

// Define validateCart in global scope
function validateCart(event, productId) {
  if (event) event.preventDefault(); // Ensure event is properly handled

  let tableSelector = document.getElementById("table-selector");
  let selectedTable = tableSelector ? tableSelector.value : null;
  let sizeInput = document.getElementById(`size-${productId}`);

  console.log("Selected Table ID:", selectedTable);
  console.log("Size Input Value:", sizeInput ? sizeInput.value : "Not Found");

  if (!selectedTable) {
    alert("Please select a table first.");
    return false;
  }

  // ✅ If no size is selected, auto-select "Medium"
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

  // If all conditions are met, submit the form
  let form = document.getElementById(`add-to-cart-form-${productId}`);
  if (form) {
    let tableField = form.querySelector('input[name="table_id"]');
    let sizeField = form.querySelector('input[name="size"]');

    if (tableField) tableField.value = selectedTable; // ✅ Ensure `table_id` is set
    if (sizeField) sizeField.value = sizeInput.value; // ✅ Ensure `size` is set

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

  function updateCartSummary(price) {
    let currentCount = parseInt(cartItemsCount.textContent);
    let currentTotal = parseFloat(cartTotalPrice.textContent.replace("₹", ""));

    cartItemsCount.textContent = currentCount + 1;
    cartTotalPrice.textContent = "₹" + (currentTotal + price).toFixed(2);
  }

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


// document.addEventListener("DOMContentLoaded", function () {
//   let selectedTable = null;
//   let cart = {};

//   // Handle Table Selection
//   document
//     .getElementById("table-selector")
//     .addEventListener("change", function () {
//       selectedTable = this.value;
//     });

//   // Select Size
//   function selectSize(productId, size) {
//     const buttons = document.querySelectorAll(
//       `[onclick^="selectSize('${productId}']`
//     );
//     buttons.forEach((btn) => btn.classList.remove("active"));
//     event.target.classList.add("active");
//   }

//   // Update Quantity
//   function updateQuantity(productId, change) {
//     const quantitySpan = document.getElementById(`quantity-${productId}`);
//     let currentQuantity = parseInt(quantitySpan.textContent, 10) || 1;
//     let newQuantity = currentQuantity + change;

//     if (newQuantity >= 1) {
//       quantitySpan.textContent = newQuantity;
//     }
//   }

//   // Add to Cart
//   function addToCart(productId) {
//     if (!selectedTable) {
//       alert("Please select a table in card-container");
//       return;
//     }

//     const productCard = document
//       .querySelector(`[onclick="addToCart('${productId}')"]`)
//       .closest(".card");
//     const productName = productCard.querySelector(".card-title").textContent;
//     const productPrice = parseFloat(
//       productCard.querySelector(".card-text").textContent.replace("₹", "")
//     );
//     const quantity = parseInt(
//       document.getElementById(`quantity-${productId}`).textContent,
//       10
//     );

//     if (!cart[productId]) {
//       cart[productId] = {
//         name: productName,
//         price: productPrice,
//         quantity: quantity,
//       };
//     } else {
//       cart[productId].quantity += quantity;
//     }

//     updateCartDisplay();
//   }

//   // Update Cart Display
//   function updateCartDisplay() {
//     const cartContainer = document.getElementById("cart-container");
//     const cartItemsCount = document.getElementById("cart-items-count");
//     const cartTotalPrice = document.getElementById("cart-total-price");

//     cartContainer.innerHTML = "";
//     let totalItems = 0;
//     let totalPrice = 0;

//     for (const productId in cart) {
//       const item = cart[productId];
//       totalItems += item.quantity;
//       totalPrice += item.price * item.quantity;

//       const cartItem = document.createElement("div");
//       cartItem.classList.add(
//         "cart-item",
//         "d-flex",
//         "justify-content-between",
//         "align-items-center"
//       );
//       cartItem.innerHTML = `
//                 <span>${item.name} x ${item.quantity}</span>
//                 <strong>₹${(item.price * item.quantity).toFixed(2)}</strong>
//             `;
//       cartContainer.appendChild(cartItem);
//     }

//     cartItemsCount.textContent = totalItems;
//     cartTotalPrice.textContent = `₹${totalPrice.toFixed(2)}`;
//   }

//   // Attach functions to global scope
//   window.selectSize = selectSize;
//   window.updateQuantity = updateQuantity;
//   window.addToCart = addToCart;
// });

// function filterProducts(category, element, event) {
//   if (event) {
//     event.preventDefault();
//   }

//   let selectedCategory = category.trim().toLowerCase();
//   console.log("Filtering products for category:", selectedCategory);

//   // Remove 'active' class from all category links
//   document.querySelectorAll(".category-link").forEach((link) => {
//     link.classList.remove("active");
//   });

//   // Add 'active' class to the clicked link
//   element.classList.add("active");

//   // Get all product elements
//   let products = document.querySelectorAll("#product-container .col-md-6");

//   products.forEach((product) => {
//     let productCategory = product
//       .getAttribute("data-category")
//       ?.trim()
//       .toLowerCase();
//     console.log("Product Category:", productCategory);

//     if (selectedCategory === "all" || productCategory === selectedCategory) {
//       product.classList.add("show");
//       product.style.display = ""; // Reset to default (ensures flex/grid works)
//     } else {
//       product.classList.remove("show");
//       product.style.display = "none"; // Hide non-matching products
//     }
//   });
// }

// // Ensure JavaScript runs after DOM is fully loaded
// document.addEventListener("DOMContentLoaded", function () {
//   document.querySelectorAll(".category-link").forEach((link) => {
//     link.addEventListener("click", function (event) {
//       filterProducts(this.textContent.trim(), this, event);
//     });
//   });
// });

// document.addEventListener("DOMContentLoaded", function () {
//   const someElement = document.getElementById("your-element-id");
//   if (someElement) {
//     someElement.addEventListener("click", function () {
//       console.log("Button clicked");
//     });
//   }
// });

// const staticPath = "/static/images";
// const categories = ["All", "Italian", "Mexican", "Beverages"];
// const products = [
//     { id: 1, name: "Pasta", price: 500, category: "Italian", image: "pasta.jpg" },
//     { id: 2, name: "Nachos", price: 350, category: "Mexican", image: "nachos.jpg" },
//     { id: 3, name: "Mint Mojito", price: 220, category: "Beverages", image: "mint-mojito.jpeg" }
// ];

// let selectedCategory = "All";
// let selectedTable = null;
// let cartData = {}; // Store cart data for each table

// // Initialize cart data for each table
// function initializeCartData() {
//     for (let i = 1; i <= 5; i++) {
//         cartData[i] = {}; // Each table has its own empty cart
//     }
// }
// initializeCartData();

// function renderCategories() {
//     const container = document.getElementById("category-container");
//     container.innerHTML = categories.map(category => `
// <div class="col-12 col-sm-6 col-md-4 col-lg-2 text-center category-col">
//     <a href="#" class="category-link ${selectedCategory === category ? 'active' : ''}"
//        onclick="filterProducts('${category}')">${category}</a>
// </div>
//     `).join("");
// }

// function filterProducts(category) {
//     selectedCategory = category;
//     renderCategories();
//     renderProducts();
// }

// function renderProducts() {
//     const container = document.getElementById("product-container");
//     const filteredProducts = selectedCategory === "All" ? products : products.filter(p => p.category === selectedCategory);

//     container.innerHTML = filteredProducts.map(product => {
//         let cartItem = selectedTable && cartData[selectedTable][product.id] ? cartData[selectedTable][product.id] : { size: null, quantity: 1 };

//         return `
//         <div class="col-md-6 mb-4 d-flex justify-content-center">
//             <div class="card d-flex flex-row align-items-center p-3" style="width: 100%;">
//                 <img src="${staticPath}/${product.image}" class="card-img-left" style="width: 100px; height: 100px; object-fit: cover; border-radius: 10px;">
//                 <div class="card-body d-flex flex-column">
//                     <h4 class="card-title">${product.name}</h4>
//                     <p class="card-text">₹${product.price}</p>

//                     <!-- Size Options -->
//                     <div class="size-options mb-2">
//                         <button class="btn btn-sm btn-outline-secondary size-btn small-btn ${cartItem.size === 'Small' ? 'selected-size' : ''}" onclick="selectSize(${product.id}, 'Small')">Small</button>
//                         <button class="btn btn-sm btn-outline-secondary size-btn medium-btn ${cartItem.size === 'Medium' ? 'selected-size' : ''}" onclick="selectSize(${product.id}, 'Medium')">Medium</button>
//                         <button class="btn btn-sm btn-outline-secondary size-btn large-btn ${cartItem.size === 'Large' ? 'selected-size' : ''}" onclick="selectSize(${product.id}, 'Large')">Large</button>
//                     </div>

//                     <!-- Quantity Selector -->
//                     <div class="d-flex align-items-center">
//                         <button class="btn btn-sm btn-outline-secondary" onclick="updateQuantity(${product.id}, -1)">-</button>
//                         <span class="mx-2" id="quantity-${product.id}">${cartItem.quantity}</span>
//                         <button class="btn btn-sm btn-outline-secondary" onclick="updateQuantity(${product.id}, 1)">+</button>
//                     </div>

//                     <!-- Add to Cart Button -->
//                     <button class="btn add-to-cart-button mt-2" id="add-to-cart-${product.id}" onclick="addToCart(${product.id})"
//                         style="background-color: ${cartItem.size ? '#f9c784' : '#4E598C'}; color: ${cartItem.size ? 'black' : 'white'};">
//                         ${cartItem.size ? "Added to Cart" : "Add to Cart"}
//                     </button>
//                 </div>
//             </div>
//         </div>
//     `;
//     }).join("");
// }

// document.getElementById("table-selector").addEventListener("change", function() {
//     selectedTable = this.value;
//     updateCart();
//     renderProducts();
// });

// function selectSize(productId, size) {
//     if (!selectedTable) {
//         alert("Please select a table first!");
//         return;
//     }

//     if (!cartData[selectedTable][productId]) {
//         cartData[selectedTable][productId] = { size: size, quantity: 1 };
//     } else {
//         cartData[selectedTable][productId].size = size;
//     }

//     renderProducts();
// }

// function updateQuantity(productId, change) {
//     if (!selectedTable || !cartData[selectedTable][productId]) return;

//     cartData[selectedTable][productId].quantity = Math.max(1, cartData[selectedTable][productId].quantity + change);
//     document.getElementById(`quantity-${productId}`).innerText = cartData[selectedTable][productId].quantity;
//     updateCart();
// }

// function addToCart(productId) {
//     if (!selectedTable) {
//         alert("Please select a table before adding items to the cart!");
//         return;
//     }

//     if (!cartData[selectedTable][productId] || !cartData[selectedTable][productId].size) {
//         alert("Please select a size before adding to cart!");
//         return;
//     }

//     updateCart();
//     renderProducts();
// }

// function updateCart() {
//     const container = document.getElementById("cart-container");
//     let totalPrice = 0;
//     let totalItems = 0;

//     if (!selectedTable || Object.keys(cartData[selectedTable]).length === 0) {
//         container.innerHTML = "<p class='text-center'>Cart is empty</p>";
//         document.getElementById("cart-total-price").innerText = `₹0.00`;
//         document.getElementById("cart-items-count").innerText = 0;
//         return;
//     }

//     container.innerHTML = `
//         <p><strong>Table: </strong> ${selectedTable || "Not selected"}</p>
//         ${Object.keys(cartData[selectedTable]).map(productId => {
//             let item = cartData[selectedTable][productId];
//             let product = products.find(p => p.id == productId);
//             let itemTotal = product.price * item.quantity;
//             totalPrice += itemTotal;
//             totalItems += item.quantity;

//             return `
//             <div class="cart-item d-flex">
//                 <img src="${staticPath}/${product.image}" class="cart-item-img">
//                 <div class="cart-item-info">
//                     <strong>${product.name}</strong><span>(${item.size})</span>
//                     <p>₹${product.price} x ${item.quantity}</p>
//                     <div class="cart-item-controls">
//                         <button onclick="updateQuantity(${product.id}, -1)">-</button>
//                         <span>${item.quantity}</span>
//                         <button onclick="updateQuantity(${product.id}, 1)">+</button>
//                     </div>
//                 </div>
//                 <button class="btn" onclick="removeFromCart(${product.id})">
//                     <i class="fa-solid fa-xmark"></i>
//                 </button>
//             </div>
//             `;
//         }).join("")}
//     `;

//     document.getElementById("cart-total-price").innerText = `₹${totalPrice.toFixed(2)}`;
//     document.getElementById("cart-items-count").innerText = totalItems;
// }

// function removeFromCart(productId) {
//     if (!selectedTable) return;

//     delete cartData[selectedTable][productId];
//     updateCart();
//     renderProducts();
// }

// renderCategories();
// renderProducts();

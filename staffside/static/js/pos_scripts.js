document.addEventListener("DOMContentLoaded", function () {
  let selectedTable = null;
  let cart = {};

  // Handle Table Selection
  document
    .getElementById("table-selector")
    .addEventListener("change", function () {
      selectedTable = this.value;
    });

  // Select Size
  function selectSize(productId, size) {
    const buttons = document.querySelectorAll(
      `[onclick^="selectSize('${productId}']`
    );
    buttons.forEach((btn) => btn.classList.remove("active"));
    event.target.classList.add("active");
  }

  // Update Quantity
  function updateQuantity(productId, change) {
    const quantitySpan = document.getElementById(`quantity-${productId}`);
    let currentQuantity = parseInt(quantitySpan.textContent, 10) || 1;
    let newQuantity = currentQuantity + change;

    if (newQuantity >= 1) {
      quantitySpan.textContent = newQuantity;
    }
  }

  // Add to Cart
  function addToCart(productId) {
    if (!selectedTable) {
      alert("Please select a table in card-container");
      return;
    }

    const productCard = document
      .querySelector(`[onclick="addToCart('${productId}')"]`)
      .closest(".card");
    const productName = productCard.querySelector(".card-title").textContent;
    const productPrice = parseFloat(
      productCard.querySelector(".card-text").textContent.replace("₹", "")
    );
    const quantity = parseInt(
      document.getElementById(`quantity-${productId}`).textContent,
      10
    );

    if (!cart[productId]) {
      cart[productId] = {
        name: productName,
        price: productPrice,
        quantity: quantity,
      };
    } else {
      cart[productId].quantity += quantity;
    }

    updateCartDisplay();
  }

  // Update Cart Display
  function updateCartDisplay() {
    const cartContainer = document.getElementById("cart-container");
    const cartItemsCount = document.getElementById("cart-items-count");
    const cartTotalPrice = document.getElementById("cart-total-price");

    cartContainer.innerHTML = "";
    let totalItems = 0;
    let totalPrice = 0;

    for (const productId in cart) {
      const item = cart[productId];
      totalItems += item.quantity;
      totalPrice += item.price * item.quantity;

      const cartItem = document.createElement("div");
      cartItem.classList.add(
        "cart-item",
        "d-flex",
        "justify-content-between",
        "align-items-center"
      );
      cartItem.innerHTML = `
                <span>${item.name} x ${item.quantity}</span>
                <strong>₹${(item.price * item.quantity).toFixed(2)}</strong>
            `;
      cartContainer.appendChild(cartItem);
    }

    cartItemsCount.textContent = totalItems;
    cartTotalPrice.textContent = `₹${totalPrice.toFixed(2)}`;
  }

  // Attach functions to global scope
  window.selectSize = selectSize;
  window.updateQuantity = updateQuantity;
  window.addToCart = addToCart;
});

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

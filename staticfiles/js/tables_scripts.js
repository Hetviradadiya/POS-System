document.addEventListener("DOMContentLoaded", function () {
  const allTables = document.querySelector("#allTables .d-flex");
  const vacantTabContent = document.querySelector("#vacant .d-flex");
  const occupiedTabContent = document.querySelector("#occupied .d-flex");
  const reservedTabContent = document.querySelector("#reserved .d-flex");
  const addTableButton = document.querySelector(".add-table-button");
  const formPopup = document.getElementById("myForm");
  const overlay = document.getElementById("overlay");
  const closeButton = document.querySelector(".btn-close");
  const addTableCards = document.querySelectorAll(".add-table-card");

  if (!addTableButton || !formPopup || !overlay || !allTables) {
    console.error("Missing elements in DOM");
    return;
  }

  // Open & Close Form Functions
  function openForm() {
    formPopup.style.display = "block";
    overlay.style.display = "block";
    addTableButton.innerHTML = `<span class="btn-text">
            <i class="fa-solid fa-xmark plus-icon"></i> Close
        </span>
        <span class="btn-icon"><i class="fa-solid fa-xmark plus-icon"></i></span>`;
  }

  function closeForm() {
    formPopup.style.display = "none";
    overlay.style.display = "none";
    addTableButton.innerHTML = `<span class="btn-text">
            <i class="fa-solid fa-plus plus-icon"></i> Add Table
        </span>
        <span class="btn-icon"><i class="fa-solid fa-plus plus-icon"></i></span>`;
  }

  // Add click event for Add Table button
  addTableButton.addEventListener("click", function () {
    if (formPopup.style.display === "block") {
      closeForm();
    } else {
      openForm();
    }
  });

  // Close form on close button or overlay click
  closeButton.addEventListener("click", closeForm);
  overlay.addEventListener("click", closeForm);
  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
      closeForm();
    }
  });

  // Function to Add Table
  function addTableCard(tableCard) {
    const newTableCard = tableCard.cloneNode(true);
    newTableCard.classList.remove("add-table-card");
    newTableCard.classList.add("table-card");

    // Add to "All Tables"
    allTables.appendChild(newTableCard);

    // Get Table Status & Add to Correct Tab
    let status = newTableCard.getAttribute("data-status");
    if (status === "vacant") {
      vacantTabContent.appendChild(newTableCard.cloneNode(true));
    } else if (status === "occupied") {
      occupiedTabContent.appendChild(newTableCard.cloneNode(true));
    } else if (status === "reserved") {
      reservedTabContent.appendChild(newTableCard.cloneNode(true));
    }

    // Attach Click Event to Open Modal
    newTableCard.addEventListener("click", function () {
      openTableModal(newTableCard);
    });
  }

  // Click event for selecting a table card from the form
  addTableCards.forEach((card) => {
    card.addEventListener("click", function () {
      addTableCard(card);
    });
  });

  // Function to Open Modal with Table Details
  function openTableModal(card) {
    const tableNumber = card.getAttribute("data-table-number");
    const tableStatus = card.getAttribute("data-status");
    const numPeople = card.getAttribute("data-num-people");
    let orderedItems = card.getAttribute("data-ordered-items");

    try {
      orderedItems = JSON.parse(orderedItems);
    } catch (e) {
      orderedItems = [];
    }

    document.getElementById("modalTableNumber").textContent = tableNumber;
    document.getElementById("modalTableStatus").textContent = tableStatus;
    document.getElementById("modalNumPeople").textContent = numPeople;

    const orderedItemsList = document.getElementById("modalOrderedItems");
    orderedItemsList.innerHTML = "";

    if (orderedItems.length > 0) {
      orderedItems.forEach((item) => {
        const li = document.createElement("li");
        li.textContent = item;
        orderedItemsList.appendChild(li);
      });
    } else {
      const li = document.createElement("li");
      li.textContent = "No orders";
      orderedItemsList.appendChild(li);
    }

    const tableModal = new bootstrap.Modal(
      document.getElementById("tableDetailsModal")
    );
    tableModal.show();
  }

  // Keep added tables when form closes
  closeButton.addEventListener("click", function () {
    formPopup.style.display = "none";
    overlay.style.display = "none";
  });

  // Prevent tables from disappearing when closing form
  overlay.addEventListener("click", function (event) {
    if (event.target === overlay) {
      formPopup.style.display = "none";
      overlay.style.display = "none";
    }
  });

  // Ensure Tables Stay in Correct Tab When Switching
  document.querySelectorAll(".nav-link").forEach((tab) => {
    tab.addEventListener("click", function () {
      let selectedTab = this.getAttribute("href").substring(1);

      // Remove active class from all tabs
      document
        .querySelectorAll(".nav-link")
        .forEach((link) => link.classList.remove("active"));
      this.classList.add("active");

      // Hide all tab content
      document
        .querySelectorAll(".tab-pane")
        .forEach((tabContent) => tabContent.classList.remove("show", "active"));

      // Show only the selected tab
      document.getElementById(selectedTab).classList.add("show", "active");

      // Move tables based on status
      if (selectedTab === "vacant") {
        vacantTabContent.innerHTML = "";
        document.querySelectorAll(".table-card.vacant").forEach((table) => {
          vacantTabContent.appendChild(table.cloneNode(true));
        });
      } else if (selectedTab === "occupied") {
        occupiedTabContent.innerHTML = "";
        document.querySelectorAll(".table-card.occupied").forEach((table) => {
          occupiedTabContent.appendChild(table.cloneNode(true));
        });
      } else if (selectedTab === "reserved") {
        reservedTabContent.innerHTML = "";
        document.querySelectorAll(".table-card.reserved").forEach((table) => {
          reservedTabContent.appendChild(table.cloneNode(true));
        });
      }
    });
  });
});

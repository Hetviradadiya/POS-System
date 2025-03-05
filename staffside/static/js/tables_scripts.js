
document.addEventListener("DOMContentLoaded", function () {
  const allTables = document.querySelector("#allTables .d-flex");
  const vacantTabContent = document.querySelector("#vacant .d-flex");
  const occupiedTabContent = document.querySelector("#occupied .d-flex");
    const reservedTabContent = document.querySelector("#reserved .d-flex");

  document.querySelectorAll(".nav-link").forEach((tab) => {
    tab.addEventListener("click", function () {
      let selectedTab = this.getAttribute("href").substring(1); // Get tab ID

      // Remove active class from all tabs
      document
        .querySelectorAll(".nav-link")
        .forEach((link) => link.classList.remove("active"));
      this.classList.add("active"); // Add active class to the clicked tab

      // Hide all tab content
      document.querySelectorAll(".tab-pane").forEach((tabContent) => {
        tabContent.classList.remove("show", "active");
      });

      // Show only the selected tab
      document.getElementById(selectedTab).classList.add("show", "active");

      // If Vacant tab is clicked, move only vacant tables
      if (selectedTab === "vacant") {
        vacantTabContent.innerHTML = ""; // Clear previous content
        document.querySelectorAll(".table-card.vacant").forEach((table) => {
          vacantTabContent.appendChild(table.cloneNode(true));
        });
      }

      // If Occupied tab is clicked, move only occupied tables
      if (selectedTab === "occupied") {
        occupiedTabContent.innerHTML = ""; // Clear previous content
        document.querySelectorAll(".table-card.occupied").forEach((table) => {
          occupiedTabContent.appendChild(table.cloneNode(true));
        });
      }

      if (selectedTab === "reserved") {
        reservedTabContent.innerHTML = ""; // Clear previous content
        document.querySelectorAll(".table-card.reserved").forEach((table) => {
          reservedTabContent.appendChild(table.cloneNode(true));
        });
      }
    });
  });
});

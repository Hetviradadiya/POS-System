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


document
  .getElementById("tableForm")
  .addEventListener("submit", function (event) {
    var selectedSeats = document.getElementById("selectedSeats").value;

    // console.log("Form submitted! Selected seats:", selectedSeats); // Debugging

    if (!selectedSeats) {
      alert("Please select a table type before adding.");
      event.preventDefault(); // Stop form submission if no table is selected
      return;
    }

    // console.log("Submitting form now...");
  });

function selectTable(event, seats) {
  event.preventDefault(); // Prevent accidental form submission

  let formSeatsInput = document.getElementById("selectedSeats");
  if (formSeatsInput) {
    formSeatsInput.value = seats;
    // console.log("Seats set:", seats); // Debugging output

    // Explicitly submit the form after selecting a table
    document.getElementById("tableForm").submit();
  } else {
    // console.error("Hidden form seats input not found!");
  }
}

function openForm() {
  document.getElementById("myForm").style.display = "block";
  document.getElementById("overlay").style.display = "block";
}

function submitBranchForm() {
  let selectedBranch = document.getElementById("branchSelect").value;
  document.getElementById("hiddenBranchInput").value = selectedBranch;
  document.getElementById("branchForm").submit(); // Submit the form
}
function closeForm() {
  document.getElementById("myForm").style.display = "none";
  document.getElementById("overlay").style.display = "none";
}

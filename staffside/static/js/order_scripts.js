document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".btn-print").forEach(function (button) {
    button.addEventListener("click", function () {
      let tableId = this.getAttribute("data-table-id");
      if (tableId) {
        window.location.href = `/staffside/bill_page/${tableId}/`; // Redirect to bill page
      }
    });
  });
});


document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".btn-pay").forEach((button) => {
    button.addEventListener("click", function () {
      let tableId = this.getAttribute("data-tableid");
      let amount = this.getAttribute("data-amount");
      let status = this.getAttribute("data-status");
      let orderId = this.getAttribute("data-orderid"); // Get order ID

      // Update modal content
      document.getElementById("payTable").textContent = tableId;
      document.getElementById("payAmount").textContent = amount;
      document.getElementById("payStatus").textContent = status;

      // Set order ID in hidden input
      document.getElementById("orderIdInput").value = orderId;

      // Show the modal
      let payModal = new bootstrap.Modal(document.getElementById("payModal"));
      payModal.show();
    });
  });
  // Ensure modal and backdrop are properly removed when closed
  document
    .getElementById("payModal")
    .addEventListener("hidden.bs.modal", function () {
      document.body.classList.remove("modal-open"); // Remove Bootstrap modal-open class
      let backdrop = document.querySelector(".modal-backdrop");
      if (backdrop) {
        backdrop.remove(); // Remove the modal overlay
      }
    });
});





// Save Edit Changes (simulated)
function saveChanges() {
  let newName = document.getElementById("edit-name").value;
  let newPrice = document.getElementById("edit-price").value;

  if (newName && newPrice) {
    alert("Order updated:\nName: " + newName + "\nPrice: ₹" + newPrice);
    closeEditBox();
  } else {
    alert("Please fill in all fields.");
  }
}

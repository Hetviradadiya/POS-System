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

      document.getElementById("discountInput").value = "";

      // Store table ID in hidden input
      document.getElementById("printTableIdInput").value = tableId;
    });
  });

  // Handle Confirm button click (ensure discount is sent)
  document
    .getElementById("confirmPayment")
    .addEventListener("click", function () {
      let discountValue = document.getElementById("discountInput").value;

      // If no discount entered, set to 0
      if (discountValue.trim() === "") {
        document.getElementById("discountInput").value = "0";
      }

      // Submit the form
      document.getElementById("paymentForm").submit();
    });

  // Automatically trigger print after form submission
  let printTableId = document.getElementById("printTableIdInput").value;
  const tableId = "{{ table_id }}";
  localStorage.removeItem(`order_type_table_${tableId}`);
  localStorage.removeItem(`customer_table_${tableId}`);
  if (printTableId) {
    let printButton = document.querySelector(
      `.btn-print[data-table-id="${printTableId}"]`
    );
    if (printButton) {
      printButton.click();
    }
  }

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

function openPOS(tableId) {
  if (tableId) {
    window.location.href = `/staffside/pos?table_id=${tableId}`;
  } else {
    window.location.href = `/staffside/pos`;
  }
}

document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".btn-edit").forEach((button) => {
    button.addEventListener("click", function () {
      let tableId = this.getAttribute("data-tableid"); // Get table_id from button
      openPOS(tableId);
    });
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

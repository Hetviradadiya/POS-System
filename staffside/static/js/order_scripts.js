$(document).ready(function () {
  // Pay button logic
  $(".btn-pay").click(function () {
    let customerName = $(this).data("customer");
    let amount = $(this).data("amount");

    $("#payCustomer").text(customerName);
    $("#payAmount").text(amount);
  });
});

// Open Edit Box with existing values
function openEditBox(name, price) {
  document.getElementById("edit-name").value = name;
  document.getElementById("edit-price").value = price;
  document.getElementById("overlay").style.display = "block";
  document.getElementById("edit-box").style.display = "block";
}

// Close Edit Box
function closeEditBox() {
  document.getElementById("overlay").style.display = "none";
  document.getElementById("edit-box").style.display = "none";
}

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

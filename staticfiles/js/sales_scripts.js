function filterTable() {
  console.log("filterTable() function called");
  var input = document.getElementById("searchInput");
  var filter = input.value.toUpperCase();
  console.log("Search value:", filter);
  
  var table = document.querySelector("table");
  if (!table) {
    console.error("Table element not found!");
    return;
  }
  var tr = table.getElementsByTagName("tr");
  
//   Loop through table rows (skip the header row)
for (var i = 1; i < tr.length; i++) {
    var orderCell = tr[i].getElementsByTagName("td")[0];
    var customerCell = tr[i].getElementsByTagName("td")[1];
    
    var orderText = orderCell ? orderCell.textContent || orderCell.innerText : "";
    var customerText = customerCell ? customerCell.textContent || customerCell.innerText : "";
    
    console.log("Row", i, "Order:", orderText, "Customer:", customerText);
    
    if (orderText.toUpperCase().indexOf(filter) > -1 || customerText.toUpperCase().indexOf(filter) > -1) {
      tr[i].style.display = "";
    } else {
      tr[i].style.display = "none";
    }
  }
}

// Attach event listener for live search when the DOM is fully loaded
document.addEventListener("DOMContentLoaded", function() {
  var searchInput = document.getElementById("searchInput");
  if (searchInput) {
    searchInput.addEventListener("keyup", filterTable);
  } else {
    console.error("Search input not found!");
  }
}); 


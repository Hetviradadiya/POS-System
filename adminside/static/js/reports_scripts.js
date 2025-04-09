function toggleSearch() {
    let searchContainer = document.querySelector(".search-container");
    let searchInput = document.querySelector(".search-input");
  
    searchContainer.classList.toggle("active");
    if (searchContainer.classList.contains("active")) {
      searchInput.focus();
    }
  } 
document.addEventListener("DOMContentLoaded", function () {
    const modal = new bootstrap.Modal(document.getElementById("detailsModal"));
    

    document.querySelectorAll(".paymentnow").forEach(button => {
        button.addEventListener("click", function () {
            // Fetch data attributes
            const total = this.getAttribute("data-total");
            const balance = this.getAttribute("data-balance");
            const date = this.getAttribute("data-date");
            const invoice = this.getAttribute("data-invoice");
            const paid = this.getAttribute("data-paid");


            // Set modal values
            document.getElementById("modal-total").textContent = `₹${total}`;
            document.getElementById("modal-paid").textContent = `₹${paid}`;
            document.getElementById("modal-balance").textContent = `₹${balance}`;
            document.getElementById("modal-due").textContent = `₹${total-paid}`;

            // Store invoice number in submit button for reference
            document.getElementById("submit-payment").setAttribute("data-invoice", invoice);

            // Show modal
            modal.show();
        });
    });

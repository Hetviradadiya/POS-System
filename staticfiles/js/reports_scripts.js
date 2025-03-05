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

    // Handle Payment Submission
    document.getElementById("submit-payment").addEventListener("click", function () {
        const invoice = this.getAttribute("data-invoice");
        const amount = document.getElementById("payment-amount").value;

        if (!amount ||amount<=0)  {
            alert("Please enter a valid payment amount.");
            return;
        }
        

        // Send data to backend via AJAX
        fetch("/process_payment/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")  // Ensure CSRF token is included
            },
            body: JSON.stringify({ invoice: invoice, amount: amount })
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);  // Show success message
            modal.hide();  // Close modal after submission
        })
        .catch(error => console.error("Error:", error));
    });
    

    // Function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});


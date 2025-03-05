    
document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".payment-btn").forEach(button => {
        button.addEventListener("click", function() {
            let invoiceNo = this.dataset.invoice;
            
            // Fetch order details from Django backend
            fetch(`/get_payment_details/${invoiceNo}/`)
            .then(response => response.json())
            .then(data => {
                // Populate modal with fetched data
                document.getElementById("modal-invoice").innerText = data.invoice_no;
                document.getElementById("modal-fullname").innerText = data.full_name;
                document.getElementById("modal-phone").innerText = data.phone;
                document.getElementById("modal-email").innerText = data.email;
                document.getElementById("modal-total").innerText = data.total;
                document.getElementById("modal-paid").innerText = data.paid;
                document.getElementById("modal-balance").innerText = data.balance;
                document.getElementById("modal-date").innerText = data.date;
                
                // Show the modal
                let paymentModal = new bootstrap.Modal(document.getElementById("paymentModal"));
                paymentModal.show();
            })
            .catch(error => console.error("Error fetching payment details:", error));
        });
    });

    // Handle Pay Now button click
    document.getElementById("pay-now-btn").addEventListener("click", function() {
        let invoiceNo = document.getElementById("modal-invoice").innerText;
        let amount = document.getElementById("payment-amount").value;

        if (!amount || amount <= 0) {
            alert("Please enter a valid payment amount.");
            return;
        }

        fetch(`/make_payment/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": "{{ csrf_token }}"
            },
            body: JSON.stringify({ invoice_no: invoiceNo, amount: amount })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("Payment Successful!");
                location.reload(); // Reload page to update table
            } else {
                alert("Payment Failed: " + data.message);
            }
        })
        .catch(error => console.error("Error processing payment:", error));
    });
});



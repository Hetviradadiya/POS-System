let currentRow = null; 
let categoryId = 1; 

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("foodItemForm").addEventListener("submit", function (event) {
        event.preventDefault();
        saveCategory();
    });
});


function toggleSearch() {
    let searchContainer = document.querySelector(".search-container");
    let searchInput = document.querySelector(".search-input");
    
    searchContainer.classList.toggle("active");
    if (searchContainer.classList.contains("active")) {
        searchInput.focus();
    }
}

// Search function
document.getElementById("searchInput").addEventListener("keyup", function () {
    let filter = this.value.trim().toLowerCase();
    let rows = document.querySelectorAll("#foodTableBody tr");
    
    rows.forEach(function (row) {
        let itemname = row.cells[1].textContent.trim().toLowerCase();
        if (itemname.includes(filter)) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }
    });
});

// Function to add or update a category
function saveCategory() {
    let itemName = document.getElementById("itemName").value.trim();
    let nameError = document.getElementById("nameError");
    
    nameError.textContent = "";
    if (!itemName) {
        nameError.textContent = "Category name is required.";
        return;
    }
    
    if (currentRow) {
        // If updating an existing row
        currentRow.cells[1].innerText = itemName;
    } else {
        // Creating a new row
        let newRow = document.createElement("tr");
        newRow.innerHTML = `
            <td>${categoryId}</td>
            <td>${itemName}</td>
            <td>
                <label class="switch">
                    <input type="checkbox" onclick="toggleStatus(this)" checked>
                    <span class="slider round"></span>
                </label>
            </td>
            <td>
                <button class="update-btn" onclick="updateRow(this)">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="delete-btn" onclick="deleteRow(this)">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        `;
        
        document.getElementById("foodTableBody").appendChild(newRow);
        categoryId++;
    }
    
    document.getElementById("foodItemForm").reset(); 
    closeForm();
    currentRow = null;
}

// Function to toggle category status
function toggleStatus(checkbox) {
    if (checkbox.checked) {
        console.log("Status: ON");
    } else {
        console.log("Status: OFF");
    }
}

function resetForm() {
    document.getElementById("foodItemForm").reset(); // Resets all input fields
}

// Function to handle updating a category
function updateRow(button) {
    currentRow = button.closest("tr");
    let name = currentRow.cells[1].innerText;
    document.getElementById("itemName").value = name;
    openForm(true);
}

// Function to delete a category row
function deleteRow(button) {
    button.closest("tr").remove();
}

// Open form modal
// function openForm() {
//     document.getElementById("overlay").style.display = "block";
//     document.getElementById("myForm").style.display = "block";
//     document.body.classList.add("popup-open");
// }
function openForm(isUpdate = false) {
    document.getElementById("overlay").style.display = "block";
    document.getElementById("myForm").style.display = "block";
    document.body.classList.add("popup-open");
  
    if (!isUpdate) {
        resetForm();  // Clears the form ONLY when adding a new chain
        updateIndex = null; // Clear any previous update reference
    }
}
// Close form modal
function closeForm() {
    document.getElementById("overlay").style.display = "none";
    document.getElementById("myForm").style.display = "none";
    document.body.classList.remove("popup-open");
   
    // Reset currentRow to prevent unintended deletions
    currentRow = null;
}

function updateProfilePic() {
    let input = document.getElementById("profile_pic");
    let file = input.files[0];

    if (file) {
        let reader = new FileReader();
        reader.onload = function (e) {
            // Update the profile picture preview
            document.getElementById("profileImage").src = e.target.result;

            // Close the modal properly
            let modalElement = document.getElementById("editProfilePicModal");
            let modalInstance = bootstrap.Modal.getInstance(modalElement);

            if (modalInstance) {
                modalInstance.hide();
            }

            // Remove the modal backdrop manually after hiding
            setTimeout(() => {
                document.querySelectorAll(".modal-backdrop").forEach(backdrop => backdrop.remove());
                document.body.classList.remove("modal-open"); // Remove the Bootstrap modal-open class
                document.body.style.overflow = "auto"; // Restore scrolling
            }, 300); // Delay slightly to match modal animation
        };

        reader.readAsDataURL(file);
    }
}
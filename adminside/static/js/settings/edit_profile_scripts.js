function updateProfilePic() {
  let formData = new FormData();
  let fileInput = document.getElementById("profile_pic");

  if (fileInput.files.length === 0) {
    alert("Please select an image.");
    return;
  }

  formData.append("profile_pic", fileInput.files[0]);

  fetch("/update-profile-pic/", {
    method: "POST",
    body: formData,
    headers: {
      "X-CSRFToken": getCSRFToken(),
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        document.getElementById("profileImage").src = data.image_url;
      } else {
        alert("Failed to update profile picture.");
      }
    })
    .catch((error) => console.error("Error:", error));
}

function getCSRFToken() {
  return document.cookie
    .split("; ")
    .find((row) => row.startsWith("csrftoken="))
    ?.split("=")[1];
}

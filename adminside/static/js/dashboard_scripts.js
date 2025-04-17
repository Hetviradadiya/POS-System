
document.addEventListener("DOMContentLoaded", function () {
  let totalIncome = document
    .getElementById("donut-chart")
    .getAttribute("data-total-income");
  let salesData = JSON.parse(
    document.getElementById("donut-chart").getAttribute("data-sales-data")
  );

  let chart = bb.generate({
    data: {
      columns: salesData,
      type: "donut",
    },
    donut: {
      title: totalIncome.toString(),
    },
    bindto: "#donut-chart",
  });
});


const bellIcon = document.querySelector(".notification");
const box = document.getElementById("notificationBox");

bellIcon.addEventListener("click", function (event) {
  event.stopPropagation(); // prevent closing on same click
  box.style.display = box.style.display === "none" ? "block" : "none";
});

document.addEventListener("click", function () {
  box.style.display = "none";
});

box.addEventListener("click", function (event) {
  event.stopPropagation(); // prevent box click from closing it
});


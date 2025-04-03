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

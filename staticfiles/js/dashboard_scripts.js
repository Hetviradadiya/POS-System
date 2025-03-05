document.addEventListener("DOMContentLoaded", function () {
    console.log("reports_scripts.js loaded!"); // Debugging check

    // Sales Chart
    const ctx = document.getElementById('salesChart');
    if (ctx) {
        new Chart(ctx.getContext('2d'), {
            type: 'line',
            data: {
                labels: ['8 AM', '10 AM', '12 PM', '2 PM', '4 PM', '6 PM', '8 PM'],
                datasets: [
                    {
                        label: 'Online Sales',
                        data: [500, 700, 1200, 900, 1300, 1700, 2000, 5000],
                        borderColor: '#6c5ce7',
                        backgroundColor: 'rgba(108, 92, 231, 0.1)',
                        tension: 0.4
                    },
                    {
                        label: 'Offline Sales',
                        data: [400, 600, 1000, 800, 1100, 1500, 1900, 4000],
                        borderColor: '#ff7675',
                        backgroundColor: 'rgba(255, 118, 117, 0.1)',
                        tension: 0.4
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    }
                },
                scales: {
                    x: { grid: { display: false } },
                    y: { grid: { display: true, color: '#eee' } }
                }
            }
        });
    } else {
        console.error("salesChart element not found!");
    }

    // Donut Chart
    let chart = bb.generate({
        data: {
            columns: [
                ["Food", 4],
                ["Drinks", 2],
                ["Other", 3],
            ],
            type: "donut",
            onclick: function (d, i) {
                console.log("onclick", d, i);
            },
            onover: function (d, i) {
                console.log("onover", d, i);
            },
            onout: function (d, i) {
                console.log("onout", d, i);
            },
        },
        donut: {
            title: "5000",
        },
        bindto: "#donut-chart",
    });
});

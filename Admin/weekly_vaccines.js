document.addEventListener("DOMContentLoaded", async function() {
    // Select the canvas element by its ID
    const ctx = document.getElementById('drugSalesChart').getContext('2d');

    // Initialize the Chart.js line chart
    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [], // Initially empty
            datasets: [{
                label: 'Vaccines Administered',
                data: [], // Initially empty
                fill: false,
                borderColor: 'rgba(75, 192, 192, 1)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Date'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Quantity Administered'
                    },
                    beginAtZero: true
                }
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                }
            }
        }
    });

    // Function to fetch drug sales data from the backend
    async function fetchDrugSalesData() {
        try {
            const url = `http://127.0.0.1:5000/drug_sales2`;
            const response = await fetch(url, { method: 'GET' });
            console.log('')

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const fetchResult = await response.json();
            console.log('Fetched drug sales data:', fetchResult); // Debugging log

            if (fetchResult.status === "success") {
                const chartData = fetchResult.data;

                // Update labels and data for the chart
                chart.data.labels = chartData.map(entry => entry.date);
                chart.data.datasets[0].data = chartData.map(entry => entry.count);
                chart.update(); // Update the chart to reflect the new data
            } else {
                console.error("Error fetching data:", fetchResult.message);
            }

        } catch (error) {
            console.error("Error fetching drug sales data:", error);
        }
    }

    // Fetch data and populate the chart after the DOM is fully loaded
    fetchDrugSalesData();
});

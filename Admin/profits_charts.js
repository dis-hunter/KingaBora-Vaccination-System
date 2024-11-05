document.addEventListener("DOMContentLoaded", async function() {
    const ctx = document.getElementById('vaccineSalesChart').getContext('2d');

    // Fetch drug sales data from the backend
    async function fetchDrugSalesData() {
        try {
            const response = await fetch('http://127.0.0.1:5000/drug_sales'); // Update with your endpoint URL if needed
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

            const salesData = await response.json();
            console.log('Drug sales data received:', salesData);

            // Prepare data arrays for labels, revenue, and profit
            const labels = [];
            const revenueData = [];
            const profitData = [];

            for (const [drugName, data] of Object.entries(salesData)) {
                labels.push(drugName);
                revenueData.push(data.total_revenue);
                profitData.push(data.profit);
            }

            // Create the bar chart to display profits
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Profits',
                        data: profitData,
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.7)',
                            'rgba(54, 162, 235, 0.7)',
                            'rgba(255, 206, 86, 0.7)',
                            'rgba(75, 192, 192, 0.7)',
                            'rgba(153, 102, 255, 0.7)'
                        ],
                        borderColor: [
                            'rgba(255, 99, 132, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 206, 86, 1)',
                            'rgba(75, 192, 192, 1)',
                            'rgba(153, 102, 255, 1)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            display: false
                        },
                        title: {
                            display: true,
                            text: 'Vaccine Revenue collected (Hover for Details)'
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    let sold = salesData[context.label].total_quantity;
                                    let profit = context.raw; // Profit amount
                                    return `Revenue: $ ${profit}, Sold: ${sold}`;
                                }
                            }
                        }
                    },
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: 'Vaccine Type'
                            }
                        },
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Revenue ($)'
                            }
                        }
                    }
                }
            });
        } catch (error) {
            console.error('Error fetching drug sales data:', error);
        }
    }

    // Fetch and render the chart data
    fetchDrugSalesData();
});

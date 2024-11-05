

document.addEventListener("DOMContentLoaded", async function() {
    // Select the canvas element by its ID
    const ctx = document.getElementById('vaccineStockChart').getContext('2d');

    try {
        // Update the fetch URL to your Flask endpoint
        const response = await fetch('http://localhost:5000/drug_inventory');
        const drugInventory = await response.json();

        // Extract labels and data from the response
        const labels = drugInventory.map(drug => drug.DrugName);
        const data = drugInventory.map(drug => drug.DrugQuantity);

        // Initialize the Chart.js bar chart
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Available Stock',
                    data: data,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.7)',
                        'rgba(54, 162, 235, 0.7)',
                        'rgba(75, 192, 192, 0.7)',
                        'rgba(255, 206, 86, 0.7)',
                        'rgba(153, 102, 255, 0.7)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(153, 102, 255, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    },
                    title: {
                        display: true,
                        text: 'Available Stock Levels for Each Vaccine'
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
                            text: 'Stock Quantity'
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error fetching drug inventory data:', error);
    }
});

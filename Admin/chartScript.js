document.addEventListener("DOMContentLoaded", async function() {
    // Select the canvas element by its ID
    const ctx = document.getElementById('drugSalesChart').getContext('2d');

    // Initialize the Chart.js line chart
    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [], // Dates will go here
            datasets: [] // Data sets for top 3 drugs will go here
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

    // Function to fetch the top administered drugs data from the backend
    async function fetchTopDrugsAdministered() {
        try {
            

            const url = `http://127.0.0.1:5000/top_drugs_administered`;
            const response = await fetch(url, { method: 'GET' });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const fetchResult = await response.json();
            console.log('Fetched top drugs administered data:', fetchResult); // Debugging log

            if (fetchResult.status === "success") {
                const chartData = fetchResult.data;

                // Create a mapping to hold the datasets for each drug
                const drugDatasets = {};

                // Populate the datasets for the top 3 drugs
                for (const [date, drugs] of Object.entries(chartData)) {
                    if (!chart.data.labels.includes(date)) {
                        chart.data.labels.push(date);
                    }
                    for (const [drug, count] of Object.entries(drugs)) {
                        if (!drugDatasets[drug]) {
                            drugDatasets[drug] = { label: drug, data: new Array(chart.data.labels.length).fill(0), borderColor: getRandomColor(), fill: false };
                            chart.data.datasets.push(drugDatasets[drug]);
                        }
                        // Find the index of the current date and update the count
                        const index = chart.data.labels.indexOf(date);
                        drugDatasets[drug].data[index] = count;
                    }
                }

                chart.update(); // Update the chart to reflect the new data
            } else {
                console.error("Error fetching data:", fetchResult.message);
            }

        } catch (error) {
            console.error("Error fetching top drugs administered data:", error);
        }
    }

    // Utility function to generate a random color for each line
    function getRandomColor() {
        const letters = '0123456789ABCDEF';
        let color = '#';
        for (let i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }

    // Fetch data and populate the chart after the DOM is fully loaded
    fetchTopDrugsAdministered();
});

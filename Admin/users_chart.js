document.addEventListener("DOMContentLoaded", async function() {
    // Select the canvas element by its ID
    const ctx = document.getElementById('doughnut').getContext('2d');

    // Initialize the Chart.js doughnut chart with initial data
    const chart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Parent', 'Child', 'Nurse', 'Admin'],
            datasets: [{
                label: 'Users',
                data: [0, 0, 0, 0], // Initial data
                borderWidth: 2,
                backgroundColor: [
                    'rgba(41,155,99,0.7)',
                    'rgba(54,162,235,0.7)',
                    'rgba(255,206,86,0.7)',
                    'rgba(120,46,139,0.7)',
                ],
                borderColor: [
                    'rgba(41,155,99,1)',
                    'rgba(54,162,235,1)',
                    'rgba(255,206,86,1)',
                    'rgba(120,46,139,1)',
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        font: { size: 14 },
                        color: '#333',
                    }
                },
                title: {
                    display: true,
                    text: 'User distribution (Hover for Details)'
                },
                tooltip: {
                    enabled: true,
                    callbacks: {
                        label: (tooltipItem) => `${tooltipItem.label}: ${tooltipItem.raw} users`,
                    }
                }
            },
            animation: {
                animateScale: true,
                animateRotate: true
            }
        }
    });

    // Function to fetch user counts from the backend and update the chart
    async function fetchUserCounts() {
        try {
            const response = await fetch('http://127.0.0.1:5000/GetUsersChart'); // Adjust the URL if necessary

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            console.log('User counts received:', data); // Debugging log

            if (data.parentCount !== undefined && data.childCount !== undefined && data.nurseCount !== undefined && data.adminCount !== undefined) {
                chart.data.datasets[0].data = [
                    data.parentCount || 0,
                    data.childCount || 0,
                    data.nurseCount || 0,
                    data.adminCount || 0
                ];
                chart.update(); // Update the chart to reflect the new data
            } else {
                console.error('Data received does not have the expected structure:', data);
            }

        } catch (error) {
            console.error('Error fetching user counts:', error);
        }
    }

    // Fetch data and update the chart after the DOM is fully loaded
    fetchUserCounts();
});

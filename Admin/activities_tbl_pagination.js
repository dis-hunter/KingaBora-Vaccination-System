let currentPage = 1;
const limit = 3;  // Set limit to 3 items per page

// Fetch activities for a specific page
function fetchActivities(page = 1) {
    fetch(`/ViewActivities?page=${page}&limit=${limit}`)
        .then(response => response.json())
        .then(data => {
            if (data.activities) {
                updateActivitiesTable(data.activities);
                currentPage = page;
                updatePaginationControls();
            } else {
                console.error(data.error);
                alert("No more activities found.");
                if (page > 1) currentPage--;  // Go back one page if no data found
            }
        })
        .catch(error => console.error('Error fetching activities:', error));
}

// Update table with fetched activities
function updateActivitiesTable(activities) {
    const tbody = document.getElementById('activitiesTableBody2');
    tbody.innerHTML = '';  // Clear previous content

    activities.forEach(activity => {
        const row = `<tr>
            <td>${activity.childName}</td>
            <td>${activity.DateofVaccination}</td>
            <td>${activity.NextVisit}</td>
            <td>${activity.nurseName}</td>
            <td>${activity.NextScheduleTime}</td>
            <td>${activity.vaccinesIssued}</td>
        </tr>`;
        tbody.innerHTML += row;
    });
}

// Navigate to the next page
function nextPage() {
    fetchActivities(currentPage + 1);
}

// Navigate to the previous page
function prevPage() {
    if (currentPage > 1) {
        fetchActivities(currentPage - 1);
    }
}

// Update pagination controls
function updatePaginationControls() {
    document.getElementById('prevButton').disabled = currentPage === 1;
    document.getElementById('pageIndicator').innerText = `Page ${currentPage}`;
}

// Fetch initial data for page 1
document.addEventListener('DOMContentLoaded', () => {
    fetchActivities();
});

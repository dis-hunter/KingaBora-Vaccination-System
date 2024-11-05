async function loadAndManageNurses() {
    try {
        const url = 'http://127.0.0.1:5000/manage_nurses';
        const response = await fetch(url, { method: 'GET' });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const nurses = await response.json();
        console.log("Nurses loaded:", nurses); // Log loaded nurses

        const table = document.getElementById('nurses-table2');
        table.innerHTML = `
            <tr>
                <th>National ID</th>
                <th>Name</th>
                <th>Contact</th>
                <th>Gender</th>
                <th>Action</th>
            </tr>
        `;

        // Populate the table with nurse data
        nurses.forEach(nurse => {
            const row = document.createElement('tr');
            row.setAttribute('data-national-id', nurse.nurseNationalID);
            row.innerHTML = `
                <td>${nurse.nurseNationalID}</td>
                <td>${nurse.nurseName}</td>
                <td>${nurse.nursephonenumber}</td>
                <td>${nurse.nurseGender}</td>
                <td>
                    <button class="action-btn delete-btn">Delete</button>
                </td>
            `;
            table.appendChild(row);
        });

        // Add event listener to handle delete actions
        table.addEventListener('click', async (event) => {
            if (event.target.classList.contains('delete-btn')) {
                const row = event.target.closest('tr');
                const nationalId = row.getAttribute('data-national-id');
                console.log("Attempting to delete nurse with ID:", nationalId);

                // Confirmation dialog
                const confirmDelete = confirm(`Are you sure you want to delete the nurse with ID ${nationalId}?`);
                if (!confirmDelete) {
                    console.log("Deletion canceled.");
                    return; // Exit the function if deletion is canceled
                }

                try {
                    const deleteUrl = `http://127.0.0.1:5000/manage_nurses/${nationalId}`;
                    const deleteResponse = await fetch(deleteUrl, { method: 'DELETE' });

                    if (!deleteResponse.ok) {
                        throw new Error(`HTTP error! Status: ${deleteResponse.status}`);
                    }

                    const result = await deleteResponse.json();
                    console.log(result.message); // Log the delete response message

                    // Remove the row from the table
                    row.remove();

                    // Redirect to dashboard with manageProfileSection loaded
                    window.location.href = "http://localhost:8080/KingaBora-Vaccination-System/Admin/admin_dashboard.html#manageProfileSection";
                } catch (deleteError) {
                    console.error('Error deleting nurse:', deleteError);
                }
            }
        });
    } catch (error) {
        console.error('Error loading nurses:', error);
    }
}

// Call the combined function when the page loads
document.addEventListener('DOMContentLoaded', loadAndManageNurses);

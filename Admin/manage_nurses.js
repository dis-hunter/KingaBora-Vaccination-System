async function loadAndManageNurses() {
    try {
        const url = 'http://127.0.0.1:5000/manage_nurses';
        const response = await fetch(url, { method: 'GET' });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const nurses = await response.json();
        console.log("Nurses loaded:", nurses); // Log loaded nurses to check data

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

        // Check if nurses array is empty
        if (nurses.length === 0) {
            console.log("No active nurses found.");
            table.innerHTML = "<tr><td colspan='5'>No active nurses found.</td></tr>";
            return; // Exit early if no active nurses
        }

        // Populate the table with nurse data
        nurses.forEach(nurse => {
            if (nurse.isActive === true) {  // Only display nurses that are active
                const row = document.createElement('tr');
                row.setAttribute('data-national-id', nurse.nurseNationalID);
                row.innerHTML = `
                    <td>${nurse.nurseNationalID}</td>
                    <td>${nurse.nurseName}</td>
                    <td>${nurse.nursephonenumber}</td>
                    <td>${nurse.nurseGender}</td>
                    <td>
                        <button class="action-btn delete-btn">Deactivate</button>
                    </td>
                `;
                table.appendChild(row);
            }
        });

        // Add event listener to handle deactivation actions
        table.addEventListener('click', async (event) => {
            if (event.target.classList.contains('delete-btn')) {
                const row = event.target.closest('tr');
                const nationalId = row.getAttribute('data-national-id');
                console.log("Attempting to deactivate nurse with ID:", nationalId);

                // Confirmation dialog
                const confirmDeactivate = confirm(`Are you sure you want to deactivate the nurse with ID ${nationalId}?`);
                if (!confirmDeactivate) {
                    console.log("Deactivation canceled.");
                    return; // Exit the function if deactivation is canceled
                }

                try {
                    const deactivateUrl = `http://127.0.0.1:5000/manage_nurses/${nationalId}`;
                    const deactivateResponse = await fetch(deactivateUrl, {
                        method: 'PATCH',  // Use PATCH instead of DELETE
                        headers: {
                            'Content-Type': 'application/json',
                        },
                    });

                    if (!deactivateResponse.ok) {
                        throw new Error(`HTTP error! Status: ${deactivateResponse.status}`);
                    }

                    const result = await deactivateResponse.json();
                    console.log(result.message); // Log the deactivation response message

                    // Check if there's a redirect URL in the response
                    if (result.redirectUrl) {
                        // Redirect to the specified URL after deactivation
                        window.location.href = result.redirectUrl;
                    } else {
                        // Update the UI: Disable the deactivate button and show the updated status
                        row.querySelector('.delete-btn').disabled = true;
                        row.querySelector('.delete-btn').innerText = 'Deactivated';
                    }

                } catch (deactivateError) {
                    console.error('Error deactivating nurse:', deactivateError);
                }
            }
        });
    } catch (error) {
        console.error('Error loading nurses:', error);
    }
}

// Call the combined function when the page loads
document.addEventListener('DOMContentLoaded', loadAndManageNurses);

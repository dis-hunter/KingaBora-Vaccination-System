/*async function viewUsers() {
    try {
        const url = 'http://127.0.0.1:5000/view_users';
        const response = await fetch(url, { method: 'GET' });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        const tableBody = document.getElementById('usersTableBody');
        tableBody.innerHTML = ''; // Clear previous rows

        data.forEach(parent => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${parent.parent_national_id}</td>
                <td>${parent.parent_name}</td>
                <td>${parent.parent_gender}</td>
                <td>${parent.parent_email}</td>
                <td>${parent.parent_contact}</td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error('Error fetching user data:', error);
    }
}*/
async function viewUsers() {
    try {
        const url = 'http://127.0.0.1:5000/view_users';
        const response = await fetch(url, { method: 'GET' });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        const tableBody = document.getElementById('usersTableBody3');
        tableBody.innerHTML = ''; // Clear previous rows

        data.forEach(parent => {
            const row = document.createElement('tr');
            const childrenNames = parent.children.length > 0 ? parent.children.join(', ') : 'No children'; // Check if there are children

            row.innerHTML = `
                <td>${parent.parent_national_id}</td>
                <td>${parent.parent_name}</td>
                <td>${childrenNames}</td>
                <td>${parent.parent_contact}</td>
                <td>${parent.parent_email}</td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error('Error fetching user data:', error);
    }
}

// Call the viewUsers function to populate the table when the page loads or on an event (e.g., button click)
document.addEventListener('DOMContentLoaded', () => {
    viewUsers();
});



async function viewSimpleUsers() {
    try {
        const url = 'http://127.0.0.1:5000/view_users_simple';
        const response = await fetch(url, { method: 'GET' });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        const tableBody = document.getElementById('simpleUsersTableBody');
        tableBody.innerHTML = ''; // Clear previous rows

        // Limit to only the first three items
        data.forEach(parent => {
            const row = document.createElement('tr');
            const childrenNames = parent.children.length > 0 ? parent.children.join(', ') : 'No children'; // Check if there are children

            row.innerHTML = `
                <td>${parent.parent_national_id}</td>
                <td>${parent.parent_name}</td>
                <td>${childrenNames}</td>
                <td>${parent.parent_contact}</td>
                
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error('Error fetching simple user data:', error);
    }
}


// Fetch and display users
viewUsers();
viewSimpleUsers();
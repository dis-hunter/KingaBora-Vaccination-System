async function ViewActivities() {
    try {
        const url = `http://127.0.0.1:5000/ViewActivities`;
        const response = await fetch(url, { method: 'GET' });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Full API Response:', data);

        const tableBody = document.getElementById("activitiesTableBody");
        console.log('Table Body:', tableBody); // Check if it finds the element

        if (Array.isArray(data.childNames) && data.childNames.length > 0) {
            tableBody.innerHTML = ''; // Clear previous rows

            data.childNames.forEach(child => {
                const childName = child.childName; 
                const vaccinesIssued = child.vaccinesIssued || []; 

                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${childName || 'N/A'}</td>
                    <td>${child.DateofVaccination || 'N/A'}</td>
                    <td>${child.NextVisit || 'N/A'}</td>
                    <td>${child.NurseName || 'N/A'}</td>
                    <td>${child.nextscheduletime || 'N/A'}</td>
                    <td>${vaccinesIssued.join(', ') || 'N/A'}</td>
                `;
                tableBody.appendChild(row);
            });
        } else {
            console.warn('No child names found in the data.');
        }
    } catch (error) {
        console.error('Error fetching activities:', error);
    }
}

async function ViewActivities2() {
    try {
        console.log("ViewAct2");
        const url = `http://127.0.0.1:5000/ViewActivities2`;
        const response = await fetch(url, { method: 'GET' });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Full API Response:', data);

        const tableBody = document.getElementById("activitiesTableBody2");
        console.log('Table Body2:', tableBody);

        if (Array.isArray(data.childNames) && data.childNames.length > 0) {
            tableBody.innerHTML = ''; // Clear previous rows

            data.childNames.forEach(child => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${child.childName || 'N/A'}</td>
                    <td>${child.DateofVaccination || 'N/A'}</td>
                    <td>${child.NextVisit || 'N/A'}</td>
                    <td>${child.NurseName || 'N/A'}</td>
                    <td>${child.nextscheduletime || 'N/A'}</td>
                    <td>${(child.vaccinesIssued || []).join(', ') || 'N/A'}</td>
                `;
                tableBody.appendChild(row);
            });
        } else {
            console.warn('No child names found in the data.');
        }
    } catch (error) {
        console.error('Error fetching activities:', error);
    }
}





// Automatically call ViewActivities when the script is loaded
ViewActivities();
ViewActivities2()

// Function to calculate a reminder date, either 7 or 14 days from today
function calculateReminderDate(daysAhead) {
    const today = new Date();
    today.setDate(today.getDate() + daysAhead);
    return today.toISOString(); // Returns the date in ISO 8601 format
}

// Function to convert the given date to ISO 8601 format with the correct timezone offset
function formatNextVisit(dateString) {
    const date = new Date(dateString);
    const timezoneOffset = -date.getTimezoneOffset(); // in minutes
    const offsetHours = Math.floor(Math.abs(timezoneOffset) / 60);
    const offsetMinutes = Math.abs(timezoneOffset) % 60;
    const sign = timezoneOffset < 0 ? '-' : '+';
    const formattedOffset = `${sign}${String(offsetHours).padStart(2, '0')}:${String(offsetMinutes).padStart(2, '0')}`;
    
    return date.toISOString().replace('Z', formattedOffset);  // Convert to ISO with timezone offset
}

// Function to fetch email list based on NextVisit date
async function getEmailList(NextVisit) {
    try {
        console.log('Getting email and parent details for NextVisit:', NextVisit);

        // Format the date correctly before sending it to the backend
        const formattedDate = formatNextVisit(NextVisit); 

        const url = `http://127.0.0.1:5000/getEmailList?NextVisit=${encodeURIComponent(formattedDate)}`;
        console.log('Request URL:', url);

        const response = await fetch(url, { method: 'GET' });
        const data = await response.json();
        console.log('Fetched data:', data);  // Log fetched data

        // Check if data was received successfully
        if (response.ok && data.data && data.data.length > 0) {
            console.log('Data received successfully:', data.data);

            const tableBody = document.getElementById('vaccination_table');
            tableBody.innerHTML = ""; // Clear previous data if any

            // Loop through and display the data in the table
            data.data.forEach(item => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${item.childName || "N/A"}</td>
                    <td>${item.parentEmailAddress || "N/A"}</td>
                    <td>${item.NextVisit || "N/A"}</td>
                    <td>${item.DateofVaccination || "N/A"}</td>
                    <td>${item.vaccinesIssued.join(", ") || "N/A"}</td>
                `;
                tableBody.appendChild(row);
            });
        } else {
            console.error('Error fetching email list or no data available:', data.error || 'No data found');
            document.getElementById('vaccineList').textContent = `Error: ${data.error || 'No data found'}`;
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('vaccineList').textContent = 'Error: ' + error.message;
    }
}


// Function to fetch email list based on NextVisit date (Alternative endpoint)
async function getEmailList2(NextVisit) {
    try {
        console.log('Fetching email and parent details for:', NextVisit);

        // Format the date correctly before sending it to the backend
        const formattedDate = formatNextVisit(NextVisit); 

        const url = `http://127.0.0.1:5000/getEmailList2?NextVisit=${encodeURIComponent(formattedDate)}`;
        console.log('Requesting:', url);

        const response = await fetch(url, { method: 'GET' });
        const data = await response.json();
        console.log('Response received:', data); // Log fetched data

        if (response.ok && data.data && data.data.length > 0) {
            console.log('Data found:', data.data);

            const tableBody = document.getElementById('vaccination_table2');
            if (!tableBody) {
                console.error('Error: Element with ID "vaccination_table2" not found.');
                return;
            }

            console.log('Clearing table content.');
            tableBody.innerHTML = ""; // Clear previous data if any

            const records = data.data.slice(0, 2); // Process only up to 2 records
            console.log('Processing these records:', records);

            records.forEach(item => {
                console.log('Adding row for:', item);

                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${item.childName || "N/A"}</td>
                    <td>${item.parentEmailAddress || "N/A"}</td>
                    <td>${item.NextVisit || "N/A"}</td>
                    <td>${item.DateofVaccination || "N/A"}</td>
                    <td>${item.vaccinesIssued.join(", ") || "N/A"}</td>
                `;
                tableBody.appendChild(row);
            });

            console.log('Table updated successfully.');
        } else {
            console.error('No valid data found:', data.error || 'Empty response');
            document.getElementById('vaccineList').textContent = `Error: ${data.error || 'No data found'}`;
        }
    } catch (error) {
        console.error('Error during API call:', error);
        document.getElementById('vaccineList').textContent = 'Error: ' + error.message;
    }
}

// Example usage with the corrected NextVisit format
getEmailList("Wed Nov 20, 2024 ");
getEmailList2("Wed Nov 20, 2024 ");

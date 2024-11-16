// Function to calculate a reminder date, either 7 or 14 days from today
function calculateReminderDate(daysAhead) {
    const today = new Date();
    today.setDate(today.getDate() + daysAhead);
    return today.toLocaleString("en-US", { timeZone: "GMT+3", dateStyle: "long", timeStyle: "medium" });
}

// Function to fetch email list based on NextVisit date

async function getEmailList(NextVisit) {
    try {
        console.log('Getting email and parent details for NextVisit:', NextVisit);

        const url = `http://127.0.0.1:5000/getEmailList?NextVisit=${encodeURIComponent(NextVisit)}`;
        console.log('Request URL:', url);

        const response = await fetch(url, { method: 'GET' });
        const data = await response.json();
        console.log('Fetched data:', data);  // Log fetched data

        if (response.ok && data.data && data.data.length > 0) {
            console.log('Email list found:', data.data);

            const tableBody = document.getElementById('vaccination_table');
            tableBody.innerHTML = ""; // Clear previous data if any

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
            console.error('Error fetching email list:', data.error || 'No data found');
            document.getElementById('vaccineList').textContent = `Error: ${data.error || 'No data found'}`;
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('vaccineList').textContent = 'Error: ' + error.message;
    }
}

async function getEmailList2(NextVisit) {
    try {
        console.log('Fetching email and parent details for:', NextVisit);

        const url = `http://127.0.0.1:5000/getEmailList2?NextVisit=${encodeURIComponent(NextVisit)}`;
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

            const records = data.data.slice(0, 2); // Process only up to 3 records
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



// Example usage
getEmailList("November 27, 2024 at 02:06:40 PM GMT+3");

getEmailList2("November 27, 2024 at 02:06:40 PM GMT+3");
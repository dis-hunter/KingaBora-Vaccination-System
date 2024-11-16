/*
async function getChildData() {
    try {
        const url = `http://127.0.0.1:5000/getChildData`;  // Your Flask endpoint URL
        const response = await fetch(url, { method: 'GET' });
        const data = await response.json();

        if (response.ok && data.data && data.data.length > 0) {
            const tableBody = document.getElementById('child_table');
            tableBody.innerHTML = ""; // Clear previous data if any

            data.data.forEach(item => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${item.localId || "N/A"}</td>
                    <td>${item.BirthCertificateID || "N/A"}</td>
                    <td>${item.ChildName || "N/A"}</td>
                    <td>${item.DateOfBirth || "N/A"}</td>
                    <td>${item.ParentName || "N/A"}</td>
                    <td><button onclick="window.location.href = 'childprog.html?id=${item.childId}'">View Child</button></td>

                `;
                tableBody.appendChild(row);
            });
        } else {
            console.error('Error fetching child data:', data.error || 'No data found');
            document.getElementById('child_table').textContent = 'No data found';
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('child_table').textContent = 'Error: ' + error.message;
    }
}

// Function to handle 'View Child' button click
function viewChild(childId) {
    // Redirect to another page for child details
    window.location.href = `/viewChildPage/${childId}`;  // Adjust URL to the page that will display child details
}

// Call the function when the DOM is fully loaded
    getChildData();  // Fetch and display the child data

    */



    async function getChildData() {
        try {
            const url = `http://127.0.0.1:5000/getChildData`;  // Your Flask endpoint URL
            const response = await fetch(url, { method: 'GET' });
            const data = await response.json();
    
            if (response.ok && data.data && data.data.length > 0) {
                const tableBody = document.getElementById('child_table');
                tableBody.innerHTML = ""; // Clear previous data if any
    
                data.data.forEach(item => {
                    const row = document.createElement("tr");
                    row.innerHTML = `
                        
                        <td>${item.BirthCertificateID || "N/A"}</td>
                        <td>${item.ChildName || "N/A"}</td>
                        <td>${item.DateOfBirth || "N/A"}</td>
                        <td>${item.ParentName || "N/A"}</td>
                        <td><button onclick="window.location.href ='childprog.html?localId=${encodeURIComponent(item.childId)}'">View Child</button></td>
    
                    `;
                    tableBody.appendChild(row);
                });
            } else {
                console.error('Error fetching child data:', data.error || 'No data found');
                document.getElementById('child_table').textContent = 'No data found';
            }
        } catch (error) {
            console.error('Error:', error);
            document.getElementById('child_table').textContent = 'Error: ' + error.message;
        }
    }
    async function getChildDataLimited() {
        try {
            console.log("Fetching limited child data...");
    
            const url = `http://127.0.0.1:5000/getChildDataLimited`; // Backend URL
            const response = await fetch(url, { method: "GET" });
            const data = await response.json();
    
            console.log("Response received from /getChildDataLimited:", data);
    
            if (response.ok && data.data && data.data.length > 0) {
                console.log("Valid data found:", data.data);
    
                const tableBody = document.getElementById("child_table_limited");
                if (!tableBody) {
                    console.error('Error: Element with ID "child_table_limited" not found.');
                    return;
                }
    
                console.log("Clearing table content...");
                tableBody.innerHTML = ""; // Clear previous data if any
    
                data.data.forEach(item => {
                    console.log("Adding row for:", item);
    
                    const row = document.createElement("tr");
                    row.innerHTML = `
                        <td>${item.BirthCertificateID || "N/A"}</td>
                        <td>${item.ChildName || "N/A"}</td>
                        <td>${item.DateOfBirth || "N/A"}</td>
                        <td>${item.ParentName || "N/A"}</td>
                        <td><button onclick="window.location.href ='childprog.html?localId=${encodeURIComponent(item.childId)}'">View Child</button></td>
                    `;
                    tableBody.appendChild(row);
                });
    
                console.log("Table updated successfully.");
            } else {
                console.error("No valid data found or empty response:", data.error || "No data found.");
                document.getElementById("child_table_limited").textContent = "No data found";
            }
        } catch (error) {
            console.error("Error during API call:", error);
            document.getElementById("child_table_limited").textContent = "Error: " + error.message;
        }
    }

    // Function to handle 'View Child' button click
    function viewChild(childId) {
        // Redirect to another page for child details
        window.location.href = `/viewChildPage/${childId}`;  // Adjust URL to the page that will display child details
    }
    
    // Call the function when the DOM is fully loaded
        getChildData();  // Fetch and display the child data
        getChildDataLimited();
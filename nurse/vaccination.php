<?php

?>

<!DOCTYPE html>
<html>
<head>
<style>
body {
  font-family: 'Playpen Sans', sans-serif;
}
.dosage {
  padding: 20px;
  border: 1px solid #ccc;
  text-align: center; 
  margin: 20px auto; /* Center the div */
  width: 50%; /* Adjust width as needed */
}
.tbody{
  border: 1px solid black;
}
#logo{
    float: left;
    margin-left: 5px;
}
.topnav {
  overflow: hidden;
  background-color: #008080;
}
h1, h2 {
  font-family: 'Playpen Sans', sans-serif;
  font-weight: 700; /* Apply the bold weight to headings */
  color: black;
}
.dosage{
  background-color: #87CEEB;
  width: 60%;
}
.tbody{
  text-align: centre;
}
tr, tbody, td, th{
    text-align: center;
    border: 2px solid black;
}
th, td {
  padding: 10px;
}
th:nth-child(2), td:nth-child(2) {
  width: 70%; /* Increase width of vaccine column */
}
th:nth-child(1), td:nth-child(1) {
  width: 40%; /* Increase width of vaccine column */
}
#update{
  background-color: #008080;
  font-size: 16px;
  color: white;
  padding: 8px 4px;
  margin: 8px 0;
  border: none;
  cursor: pointer;
  border-radius: 4px;
}
#paymentBtn{
  background-color: #008080;
  font-size: 20px;
  color: white;
  padding: 14px 20px;
  margin: 8px 0;
  border: none;
  cursor: pointer;
  width: 100%;
}
label, input{
  font-size: 12pt;
}
.date{
  border-radius:2px;
  text-align: centre;
  font-size: 12pt;
  text-decoration: bold;
  padding: 0%;
}
table{
  justify-content: center;
  transform: translate(248px,0);
}
.vaccine-column {
  text-align: left; /* Align checkboxes to the left */
}
.vaccine-checkbox {
  margin-right: 7px; /* Add spacing between checkboxes and text */
}
</style>
</head>
<body>
  <div class="topnav">
    <div>
    <img src="../img/logo.png" id="logo" alt="Software Engineering Logo" width="170" height="120">
    </div>
    <h2>Child Vaccination Profile</h2>
    <form class="d-flex" role="search" onsubmit="searchBar(); return false;">
      <input class="form-control me-2" type="search" id="searchQuery" placeholder="Enter Parent Name" aria-label="Search">
      <button class="btn btn-outline-success" type="submit">Search</button>
  </form>
  <label>Child's Name: </label>
    <input type="text" name="child_name" placeholder="Child's Name">
  <label>Parent/Guardian's name: </label>
    <input type="text" name="child_name" placeholder="Parent/Guardian's Name">
  <label>Last Visit:</label>
    <input type="text" name="lstvisit" placeholder="Last Visit">
  </div>
    <div class="main">
        <div class="date">
          <?php echo "Date: " . date("d-m-Y"); ?>
        </div>
        <div class="dosage">
        <h2>DOSAGE</h2>
    <!-- <table>
      <thead>
        <tr>
          <th>AGE</th>
          <th>VACCINE(S)</th>
        </tr>
      </thead>
      <tbody>
        <?php
        // Replace this with your actual vaccine data (from database or array)
        $vaccineData = array(
          array("Birth", "BCG, Birth Polio, HepB"),
          // array("Dosage 2", "OPV-1, Penta-1, PCV-1, Rota-1"),
          // array("Dosage 3", "OPV-2, Penta-2, PCV-2, Rota-2"),
          // ... add more dosages and vaccines
        );

        foreach ($vaccineData as $vaccine) {
          echo "<tr>";
          echo "<td>" . $vaccine[0] . "</td>";
          echo "<td class='vaccine-column'>";
          $vaccines = explode(",", $vaccine[1]);
          foreach ($vaccines as $v) {
            echo "<input type='checkbox' class='vaccine-checkbox' name='vaccine[]' value='" . trim($v) . "'> " . trim($v) . "<br>";
          }
          echo "</td>";
          echo "</tr>";
        }
        ?>
      </tbody>
    </table> -->
    <div id="graph">
    <title>Child Growth Chart</title>
<script src="https://d3js.org/d3.v7.min.js"></script>
<style>
.line {
  fill: none;
  stroke: steelblue;
  stroke-width: 2px;
}
</style>
</head>
<body>

<svg width="600" height="400"></svg>

<script>

// Set the dimensions and margins of the graph
const margin = {top: 20, right: 20, bottom: 30, left: 50},
    width = 600 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

// Parse the date / time   

const parseTime = d3.timeParse("%m/%d/%Y");

// Set the ranges
const x = d3.scaleTime().range([0, width]);
const y = d3.scaleLinear().range([height,   
 0]);

// Define the line
const valueline = d3.line()
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.weight);   
 });

// Append the svg obgect to the body of the page
// appends a 'group' element to 'svg'
// moves the 'group' element to the top left margin   

const svg = d3.select("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top   
 + ")");

// Get the data   

const data = [
  {date: "1/1/2020", weight: 7},
  {date: "4/1/2020", weight: 9},
  {date: "7/1/2020", weight: 11},
  {date: "10/1/2020", weight: 13},
  {date: "1/1/2021", weight: 15},
  {date: "4/1/2021", weight: 17},
  {date: "7/1/2021", weight: 19},
  {date: "10/1/2021", weight: 21}
];

// format the data
data.forEach(function(d) {
  d.date = parseTime(d.date);
  d.weight = +d.weight;
});

// Scale the range of the data
x.domain(d3.extent(data, function(d) { return d.date; }));
y.domain([0, d3.max(data, function(d) { return   
 d.weight; })]);

// Add the valueline path.
svg.append("path")
  .data([data])
  .attr("class", "line")
  .attr("d", valueline);

// Add the X Axis
svg.append("g")
  .attr("transform", "translate(0," + height + ")")
  .call(d3.axisBottom(x));   


// Add the Y Axis
svg.append("g")
  .call(d3.axisLeft(y));   


</script>

    </div>
    <div id="measurementsDiv">
    <h2>Measurements</h2>
    <label for="weight">Weight (kg):</label>
    <input type="number" id="weight" name="weight"><br><br>
    <label for="height">Height (cm):</label>
    <input type="number" id="height" name="height">
    <br><br>
    <button type="button" id="update">UPDATE</button>
  </div>
</div>
</div>
<button type="button" id="paymentBtn">PAYMENT</button>

  <script>
     document.querySelector("form").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent form from submitting and reloading the page
    searchBar();  // Call your async function
  });

  async function searchBar() {
    const storedLocalId = localStorage.getItem('localId');
    console.log("Stored Local ID:", storedLocalId);

    const parentName = document.getElementById('searchQuery').value;  // Get the parent name from the input field
    console.log(parentName);

    try {
      // Define the API URL and include the ParentName as a query parameter
      const url = `http://127.0.0.1:5000/childDetails?ParentName=${encodeURIComponent(parentName)}`;

      // Send a GET request to the backend
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',  // You can keep headers if needed
        }
      });

      // Process the response
      const data = await response.json();

      if (response.ok) {
        console.log('Children found:', data);  // Log child names in the console
        
        // Call a function to update the DOM with the list of children
        displayChildren(data.children); // Assuming the children are in `data.children`
      } else {
        console.error('Error fetching child details:', data.error || response.statusText);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  }
  </script>
</body>
<footer>

</footer>
</html>

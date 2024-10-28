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
    <table>
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
    </table>
    <div id="graph">
      
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
    // Add any JavaScript functionality here if needed, e.g., 
    // for handling button clicks, form submission, etc.
  </script>
</body>
<footer>

</footer>
</html>

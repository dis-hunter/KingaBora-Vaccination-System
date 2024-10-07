<?php
function displaychildvacc($conn, $page = 1, $limit = 5) {
    $offset = ($page - 1) * $limit;
    $sql = "SELECT Vaccine, DueDate, Status FROM childvaccine LIMIT $limit OFFSET $offset";
    $result = mysqli_query($conn, $sql);

    // Check if there are results
    if (mysqli_num_rows($result) > 0) {
        echo "<table border='1'>";
        echo "<tr><th>Vaccine</th><th>Due Date</th><th>Status</th></tr>";

        // Output data of each row
        while ($row = mysqli_fetch_assoc($result)) {
            echo "<tr>";
            echo "<td>" . $row["Vaccine"] . "</td>";
            echo "<td>" . $row["DueDate"] . "</td>";
            echo "<td>" . $row["Status"] . "</td>";
            echo "<td><a href='edit_details.php?id=" . $row["Id"] . "'>Edit</a> | <a href='delete_vaccine.php?id=" . $row["Id"] . "'>Delete</a></td>";
            echo "</tr>";
        }
        echo "</table>";
    } else {
        echo "0 results";
    }
}


?>


<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
    <style>
        table {
            border-collapse: collapse;
            width: 90%;
            margin-left: 5%;
        }
        th, td {
            border: 1px solid black;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
            color: #943c0d;
        }
    </style>
  </head>
  <body>
    <header></header>
    <main>
        <div>
            <div>
                <ul>
                <li><img src='' alt='Profile photo'></li>
                <li><h3>Name:</h3></li>
                <li><h3>Age:</h3></li>
                <li><h3>Edit Profile</h3></li>
                <li><h3>Emergency Contact</h3></li>
                </ul>

            </div>
            <div>
                <ul>
                <li><p>Overview</p></li>
                <li><p>Appointments</p></li>
                <li><p>Vaccination Summary</p></li>
                <ul>
            </div>
            <div>
                <?php displaychildvacc($conn, 1, 5); ?>

            </div>
        </div>
    </main>
    <footer></footer>
  </body>
  </html>
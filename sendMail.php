<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Vaccination Reminder System</title>
  
  <style>
    /* General page styling */
    body {
      font-family: Arial, sans-serif;
      background-color: #f4f4f9;
      margin: 0;
      padding: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      height: 100vh;
      color: #333;
    }

    .container {
      background-color: #fff;
      border-radius: 10px;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
      padding: 30px;
      width: 500px;
      max-width: 100%;
      text-align: center;
    }

    h1 {
      color: #2a9d8f;
      font-size: 2rem;
      margin-bottom: 20px;
    }

    button {
      background-color: #2a9d8f;
      color: white;
      padding: 15px 20px;
      font-size: 1.1rem;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      transition: background-color 0.3s ease;
      width: 100%;
      margin-top: 20px;
    }

    button:hover {
      background-color: #21867a;
    }

    button:active {
      background-color: #1a705d;
    }

    /* Loading and error states */
    .loading {
      font-size: 1.2rem;
      color: #ff6600;
      margin-top: 20px;
    }

    .error {
      font-size: 1rem;
      color: #e63946;
      margin-top: 20px;
    }

    /* Additional styles for the vaccine list output */
    #vaccineList {
      margin-top: 20px;
      font-size: 1rem;
      white-space: pre-wrap;
      word-wrap: break-word;
      max-width: 600px;
      color: #333;
      text-align: left;
      margin-top: 30px;
    }

  </style>
</head>
<body>
  <div class="container">
    <h1>Vaccination Reminder System</h1>
    <button onclick="scheduleEmailReminders()">Send Reminders for Upcoming Vaccinations</button>
    <p id="vaccineList"></p>
  </div>

  <script>
    async function getEmailList() {
      try {
        // Get today's date and add 7 days
        const today = new Date();
        today.setDate(today.getDate() + 7);  // Add 7 days to today's date

        // Format the date to "Nov 24, 2024" (with comma)
        const formattedDate = today.toLocaleString('en-US', {
          year: 'numeric',
          month: 'short',
          day: '2-digit'
        });

        console.log("Formatted date (7 days from today):", formattedDate);

        // Build the URL to call the Flask API with the formatted date
        const url = `http://127.0.0.1:5000/getEmailList`;

        // Fetch the data from the Flask API
        const response = await fetch(url, { method: 'GET' });
        const data = await response.json();

        if (response.ok) {
          // Call function to send reminder emails
          sendReminders(data.data);
        } else {
          // Log any error if response is not ok
          console.error('Error fetching email list:', data.error || response.statusText);
          document.getElementById('vaccineList').textContent = `Error: ${data.error || 'Failed to fetch emails'}`;
        }
      } catch (error) {
        // Handle any network or fetch-related errors
        console.error('Error:', error);
        document.getElementById('vaccineList').textContent = 'Error: ' + error.message;
      }
    }

    // Function to send email reminders
    async function sendReminders(emailList) {
      for (let reminder of emailList) {
        const { parentEmailAddress, childName, NextVisit } = reminder;

        try {
          // Send the email reminder via POST request to sendMail.php
          const mailResponse = await fetch('sendMail.php', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              email: parentEmailAddress,
              childName: childName,
              nextVisit: NextVisit,
            }),
          });

          const result = await mailResponse.json();
          if (result.status === 'success') {
            console.log(result.message);  // Log success message
          } else {
            console.error(result.message);  // Log error message
          }
        } catch (error) {
          console.error('Error sending email:', error);
        }
      }

      alert('Reminders sent successfully!');
    }

    // Function to schedule email reminders (14 days from today)
    function scheduleEmailReminders() {
      const today = new Date();
      today.setDate(today.getDate() + 14);

      // Format the date (Month Day, Year format)
      const formattedDate = today.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
      console.log('Formatted Date:', formattedDate);

      // Call the function to fetch the email list
      getEmailList(formattedDate);
    }
  </script>

  <?php
  // Include PHPMailer files
  require 'C:/xampp/htdocs/PHPMailer/src/PHPMailer.php';
  require 'C:/xampp/htdocs/PHPMailer/src/SMTP.php';
  require 'C:/xampp/htdocs/PHPMailer/src/Exception.php';

  use PHPMailer\PHPMailer\PHPMailer;
  use PHPMailer\PHPMailer\Exception;

  // Check if a POST request is made
  if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Get POST data
    $data = json_decode(file_get_contents('php://input'), true);

    if (isset($data['email']) && isset($data['childName']) && isset($data['nextVisit'])) {
      // Send email function
      function sendMail($recipientEmail, $childName, $nextVisitDate) {
        $mail = new PHPMailer(true);

        try {
          // SMTP settings
          $mail->isSMTP();
          $mail->Host = 'smtp.gmail.com';
          $mail->SMTPAuth = true;
          $mail->Username = 'eoringe372@gmail.com';  // Your email address
          $mail->Password = 'wdjk opaf jhdx wjjr';  // Your app password
          $mail->SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS;
          $mail->Port = 587;
          $mail->setFrom('eoringe372@gmail.com', 'Kinga Bora');
          $mail->addAddress($recipientEmail);  // Add recipient email
          $mail->isHTML(true);  // Set email format to HTML

          // Subject and body content
          $mail->Subject = "Reminder: {$childName}'s Vaccination Appointment in One Week";
          $mail->Body = "
              <p>This is a friendly reminder that your child, {$childName}, is scheduled to receive their next vaccination in one week.</p>
              <p><strong>Scheduled Date:</strong> {$nextVisitDate}</p>
              <p>Warm regards,<br>Kinga Bora Team</p>";

          // Send email
          if ($mail->send()) {
            echo json_encode(['status' => 'success', 'message' => "Reminder sent to {$recipientEmail} for {$childName}"]);
          } else {
            echo json_encode(['status' => 'error', 'message' => 'Failed to send email']);
          }
        } catch (Exception $e) {
          echo json_encode(['status' => 'error', 'message' => 'Error: ' . $e->getMessage()]);
        }
      }

      // Call the function to send the email
      sendMail($data['email'], $data['childName'], $data['nextVisit']);
    } else {
      echo json_encode(['status' => 'error', 'message' => 'Missing required parameters']);
    }
  }
  ?>
</body>
</html>

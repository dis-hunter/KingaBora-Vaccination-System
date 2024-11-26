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
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100vh;
      color: #333;
    }

    h1 {
      color: #2a9d8f;
      font-size: 2.5rem;
      margin-bottom: 20px;
    }

    table {
      width: 100%;
      border: 1px solid #ddd;
      border-collapse: collapse;
      margin-top: 20px;
    }

    th, td {
      padding: 8px;
      text-align: left;
      border: 1px solid #ddd;
    }

    th {
      background-color: #2a9d8f;
      color: white;
    }

    td {
      background-color: #f9f9f9;
    }

    button {
      background-color: #2a9d8f;
      color: white;
      padding: 10px 20px;
      font-size: 1rem;
      border: none;
      border-radius: 5px;
      cursor: pointer;
    }

    button:hover {
      background-color: #21867a;
    }
  </style>
</head>
<body>
  <h1>Vaccination Reminder System</h1>
  <button onclick="scheduleEmailReminders()">Send Reminders for Upcoming Vaccinations</button>
  
  <table id="vaccineList">
    <thead>
      <tr>
        <th>Parent Email</th>
        <th>Child Name</th>
        <th>Next Visit</th>
        <th>Vaccines Issued</th>
      </tr>
    </thead>
    <tbody>
      <!-- Data will be populated here dynamically -->
    </tbody>
  </table>

  <script>
    async function getEmailList() {
      try {
        const response = await fetch('http://127.0.0.1:5000/getEmailList');
        const data = await response.json();

        if (response.ok) {
          const tableBody = document.querySelector('#vaccineList tbody');
          tableBody.innerHTML = ''; // Clear existing rows

          data.data.forEach(reminder => {
            const row = document.createElement('tr');
            row.innerHTML = `
              <td>${reminder.parentEmailAddress}</td>
              <td>${reminder.childName}</td>
              <td>${reminder.NextVisit}</td>
              <td>${reminder.vaccinesIssued}</td>
            `;
            tableBody.appendChild(row);
          });

          sendReminders(data.data);
        } else {
          console.error('Error fetching email list:', data.error || response.statusText);
        }
      } catch (error) {
        console.error('Error:', error);
      }
    }

    async function sendReminders(emailList) {
      for (const reminder of emailList) {
        try {
          const response = await fetch('sendMail.php', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(reminder),
          });

          const result = await response.json();
          console.log(result.message);
        } catch (error) {
          console.error('Error sending email:', error);
        }
      }

      alert('Reminders sent successfully!');
    }

    function scheduleEmailReminders() {
      getEmailList();
    }
  </script>

  <?php
  require 'C:/xampp/htdocs/PHPMailer/src/PHPMailer.php';
  require 'C:/xampp/htdocs/PHPMailer/src/SMTP.php';
  require 'C:/xampp/htdocs/PHPMailer/src/Exception.php';

  use PHPMailer\PHPMailer\PHPMailer;
  use PHPMailer\PHPMailer\Exception;

  if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $data = json_decode(file_get_contents('php://input'), true);

    if (!empty($data['email']) && !empty($data['childName']) && !empty($data['nextVisit'])) {
      $mail = new PHPMailer(true);

      try {
        $mail->isSMTP();
        $mail->Host = 'smtp.gmail.com';
        $mail->SMTPAuth = true;
        $mail->Username = 'your_email@gmail.com';
        $mail->Password = 'your_app_password';
        $mail->SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS;
        $mail->Port = 587;

        $mail->setFrom('your_email@gmail.com', 'Vaccination Reminder System');
        $mail->addAddress($data['email']);
        $mail->isHTML(true);

        $mail->Subject = "Reminder: {$data['childName']}'s Vaccination";
        $mail->Body = "
          <p>Dear Parent,</p>
          <p>This is a friendly reminder about {$data['childName']}'s upcoming vaccination:</p>
          <p><strong>Scheduled Date:</strong> {$data['nextVisit']}</p>
          <p>Thank you for your attention.</p>";

        if ($mail->send()) {
          echo json_encode(['status' => 'success', 'message' => "Reminder sent to {$data['email']}"]);
        } else {
          echo json_encode(['status' => 'error', 'message' => 'Failed to send email.']);
        }
      } catch (Exception $e) {
        echo json_encode(['status' => 'error', 'message' => $e->getMessage()]);
      }
    } else {
      echo json_encode(['status' => 'error', 'message' => 'Invalid data.']);
    }
  }
  ?>
</body>
</html>

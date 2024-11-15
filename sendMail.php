<?php

require 'C:/xampp/htdocs/PHPMailer/src/PHPMailer.php';
require 'C:/xampp/htdocs/PHPMailer/src/SMTP.php';
require 'C:/xampp/htdocs/PHPMailer/src/Exception.php';

use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

class SendMail {
    private $mailer;

    public function __construct() {
        $this->mailer = new PHPMailer(true);
        $this->mailer->isSMTP();
        $this->mailer->Host = 'smtp.gmail.com';
        $this->mailer->SMTPAuth = true;
        $this->mailer->Username = 'eoringe372@gmail.com';
        $this->mailer->Password = 'wdjk opaf jhdx wjjr';
        $this->mailer->SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS;
        $this->mailer->Port = 587;
        $this->mailer->setFrom('eoringe372@gmail.com', 'KINGA BORA');
        $this->mailer->isHTML(true);
    }

    public function sendMail($recipientEmail, $childName, $nextVisitDate) {
        try {
            $subject = "Reminder: {$childName}'s Vaccination Appointment in One Week";
            $body = "
                <p>This is a friendly reminder that your child, {$childName}, is scheduled to receive their next vaccination in one week.</p>
                <p><strong>Scheduled Date:</strong> {$nextVisitDate}</p>
                <p>Warm regards,<br>Kinga Bora Team</p>";
            
            $this->mailer->addAddress($recipientEmail);
            $this->mailer->Subject = $subject;
            $this->mailer->Body = $body;

            if ($this->mailer->send()) {
                echo "Reminder sent to {$recipientEmail} for {$childName} on {$nextVisitDate}<br>";
            } else {
                echo "Failed to send email to {$recipientEmail}<br>";
            }
            $this->mailer->clearAddresses(); // clear for next iteration
            
        } catch (Exception $e) {
            echo "Error: " . $e->getMessage();
        }
    }
}

// Step 1: Define $nextVisitDate (14 days from today)
$nextVisitDate = date('F d, Y \a\t h:i:s A', strtotime('+14 days')); // Example: "November 29, 2024 at 12:00:00 PM"

// Step 2: Fetch email data from Flask endpoint
$url = "http://127.0.0.1:5000/getEmailList?NextVisit=" . urlencode($nextVisitDate);
$emailData = json_decode(file_get_contents($url), true);

if (!empty($emailData) && isset($emailData['data'])) {
    $sendMail = new SendMail();
    foreach ($emailData['data'] as $record) {
        $sendMail->sendMail(
            $record['parentEmailAddress'],
            $record['childName'],
            $record['NextVisit']
        );
    }
} else {
    echo "Error: No email data provided or invalid response.";
}
?>





<!-- <!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Vaccination Reminder System</title>
</head>
<body>
  <h1>Vaccination Reminder System</h1>
  <button onclick="scheduleEmailReminders()">Send Reminders for Upcoming Vaccinations</button>
  <p id="vaccineList"></p>

  <script>
    async function getEmailList(nextVisitDate) {
    try {
        const url = `http://127.0.0.1:5000/getEmailList?NextVisit=${encodeURIComponent(nextVisitDate)}`;
        const response = await fetch(url, { method: 'GET' });
        const data = await response.json();

        if (response.ok) {
            console.log('Email list found:', data.data);
            // Send this data to PHP for dynamic email generation
            sendDynamicEmails(data.data);
        } else {
            console.error('Error fetching email list:', data.error || response.statusText);
            document.getElementById('vaccineList').textContent = `Error: ${data.error || 'Failed to fetch emails'}`;
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('vaccineList').textContent = 'Error: ' + error.message;
    }
}

function scheduleEmailReminders() {
    const today = new Date();
    today.setDate(today.getDate() + 14);
    const options = {
        year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit',
        second: '2-digit', hour12: true, timeZone: 'Africa/Nairobi', timeZoneName: 'short'
    };
    const formattedDate = today.toLocaleString('en-US', options);
    console.log('Formatted Date:', formattedDate);
    getEmailList(formattedDate);
}

function sendDynamicEmails(emailData) {
    fetch('sendEmails.php', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ emailData })
    })
    .then(response => response.json())
    .then(result => console.log('Emails sent:', result))
    .catch(error => console.error('Error sending emails:', error));
}

  </script>
</body>
</html> -->

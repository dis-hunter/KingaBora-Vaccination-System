<?php
// session_start();
// require 'C:\xampp\htdocs\PHPMailer\src\PHPMailer.php';
// require 'C:\xampp\htdocs\PHPMailer\src\SMTP.php';
// require 'C:\xampp\htdocs\PHPMailer\src\Exception.php';
// // require 'C:\xampp\htdocs\PHPMailer\src\OAuth.php';
// require 'vendor\autoload.php';

// require 'vendor/autoload.php';

// use PHPMailer\PHPMailer\PHPMailer;
// use PHPMailer\PHPMailer\SMTP;
// use PHPMailer\PHPMailer\Exception;

// class sendMail
// {
//     public function sendVaccinationReminder($parentEmail, $childName, $childAge, $vaccineName) {
//         // Calculate the difference in weeks between today and the child's age
//         $today = new DateTime();
//         $childBirthDate = $today->sub(new DateInterval('P' . $childAge . 'Y'));
//         $interval = $today->diff($childBirthDate);
//         $weeksOld = floor($interval->days / 7);

//         // Define the reminder intervals (1 week before the due date) and messages
//         $reminders = [
//             5  => "Reminder: {$childName}'s vaccination {6-weeks} is due in 1 week.",
//             9  => "Reminder: {$childName}'s vaccination {10-weeks} is due in 1 week.",
//             13 => "Reminder: {$childName}'s vaccination {14-weeks} is due in 1 week.",
//             23 => "Reminder: {$childName}'s vaccination {6-months} is due in 1 week.",
//             27 => "Reminder: {$childName}'s vaccination {7-months} is due in 1 week.",
//             35 => "Reminder: {$childName}'s vaccination {9-months} is due in 1 week.",
//             39 => "Reminder: {$childName}'s vaccination {10-months} is due in 1 week.",
//             51 => "Reminder: {$childName}'s vaccination {1-year} is due in 1 week.",
//             63 => "Reminder: {$childName}'s vaccination {15-months} is due in 1 week.",
//             103=> "Reminder: {$childName}'s vaccination {2-years} is due in 1 week."
//         ];

//         // Check if a reminder is due at this age (1 week before)
//         if (isset($reminders[$weeksOld])) {
//             $subject = "Vaccination Reminder for {$childName}";
//             $body = $reminders[$weeksOld];

//             $mail = new PHPMailer(true);
//             try {
//                 $mail->isSMTP();
//                 $mail->Host = 'smtp.gmail.com';
//                 $mail->SMTPAuth = true;
//                 $mail->Username = 'tobikoleriari69@gmail.com';
//                 $mail->Password = 'zswt oxnd foao vwab'; // Replace with your actual password or use a more secure method
//                 $mail->SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS;
//                 $mail->Port = 587;

//                 $mail->setFrom('tobikoleriari69@gmail.com', 'Tobiko Leriari');
//                 $mail->addAddress($parentEmail);
//                 $mail->isHTML(true);
//                 $mail->Subject = $subject;
//                 $mail->Body = $body;

//                 if ($mail->send()) {
//                     echo 'Mail sent to ' . $parentEmail . ' successfully';
//                 } else {
//                     echo 'Mail not sent';
//                 }
//             } catch (Exception $e) {
//                 echo "Message could not be sent. Mailer Error: {$mail->ErrorInfo}";
//             }
//         }
//     }
// }

// // Example usage:
// $sendMail = new sendMail();
// $sendMail->sendVaccinationReminder('parent@example.com', 'John Doe', '1', 'MMR'); 

?>
<!DOCTYPE html>
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
          // Handle/display data as needed
          document.getElementById('vaccineList').innerHTML = JSON.stringify(data.data);
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
      // Get today's date, add 14 days, and format it
      const today = new Date();
      today.setDate(today.getDate() + 14);

      const options = {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: true,
        timeZone: 'Africa/Nairobi',
        timeZoneName: 'short'
      };

      const formattedDate = today.toLocaleString('en-US', options);
      console.log('Formatted Date:', formattedDate);
      getEmailList(formattedDate);
    }
  </script>
</body>
</html>

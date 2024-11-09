<?php
// Include Composer's autoload file
require 'vendor/autoload.php';
require 'C:/xampp/htdocs/PHPMailer/src/PHPMailer.php';
require 'C:/xampp/htdocs/PHPMailer/src/SMTP.php';
require 'C:/xampp/htdocs/PHPMailer/src/Exception.php';

use Google\Cloud\Firestore\FirestoreClient;
use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

class SendMail {
    private $mailer;

    public function __construct() {
        $this->mailer = new PHPMailer(true);
        
        // SMTP Configuration
        $this->mailer->isSMTP();
        $this->mailer->Host = 'smtp.gmail.com';
        $this->mailer->SMTPAuth = true;
        $this->mailer->Username = 'eoringe372@gmail.com';
        $this->mailer->Password = 'wdjk opaf jhdx wjjr';
        $this->mailer->SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS; 
        $this->mailer->Port = 587;

        // Default Sender
        $this->mailer->setFrom('eoringe372@gmail.com', 'KINGA BORA');
        $this->mailer->isHTML(true); // Enable HTML
    }

    public function sendMail($recipients, $subject, $body) {
        if (!is_array($recipients)) {
            $recipients = [$recipients];
        }
        
        $results = [];
        
        try {
            foreach ($recipients as $recipient) {
                $this->mailer->addAddress($recipient);
                $this->mailer->Subject = $subject;
                $this->mailer->Body = $body;
                
                if ($this->mailer->send()) {
                    $results[$recipient] = "Mail sent successfully";
                } else {
                    $results[$recipient] = "Failed to send mail";
                }
                
                // Clear the recipient for the next iteration
                $this->mailer->clearAddresses();
            }
            return $results;
            
        } catch (Exception $e) {
            throw new Exception("Message could not be sent. Mailer Error: {$this->mailer->ErrorInfo}");
        }
    }
}

function getEmailsFromFirestore() {
    $firestore = new FirestoreClient([
        'projectId' => 'kingaboravaccinationsystem' // Replace with your actual Firestore project ID
    ]);

    $parentDataCollection = $firestore->collection('parentData');
    $emails = [];
    $documents = $parentDataCollection->documents();

    foreach ($documents as $document) {
        if ($document->exists()) {
            $email = $document->data()['parentEmailAddress'];
            if (!empty($email)) {
                $emails[] = $email;
            }
        }
    }

    return $emails;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    try {
        $emailArray = getEmailsFromFirestore(); // Fetch emails from Firestore
        $mailer = new SendMail();
        
        $subject = "Reminder: [Child Name]'s Vaccination Appointment";
        $body = "This is a reminder that your child, [Child's Name], is scheduled to receive their next vaccination soon.
        <br><br>
        **Vaccine Information:**<br>
        - **Vaccine Name:** [Vaccine Name]<br>
        - **Scheduled Date:** [Due Date]<br>
        - **Scheduled Time:** [Due Time]<br><br>
        Warm regards,<br>
        [Your Team/Organization]<br>
        [Contact Information]<br>
        [Facility Address]";
        
        $results = $mailer->sendMail($emailArray, $subject, $body);
        
        foreach ($results as $recipient => $status) {
            echo "Recipient: $recipient - Status: $status<br>";
        }
    } catch (Exception $e) {
        echo "Error: " . $e->getMessage();
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Initiate Reminders</title>
</head>
<body>
    <h1>Initiate Vaccination Reminders</h1>
    <p>Current Date: <?php echo date('Y-m-d'); ?></p>
    <form method="POST">
        <button type="submit">Send Reminders</button>
    </form>
</body>
</html>
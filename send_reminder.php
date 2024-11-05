<?php
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

    public function sendMail($recipient, $subject, $body) {
        try {
            $this->mailer->addAddress($recipient);
            $this->mailer->Subject = $subject;
            $this->mailer->Body = $body;

            if ($this->mailer->send()) {
                return "Mail sent successfully to {$recipient}";
            } else {
                return "Failed to send mail to {$recipient}";
            }
        } catch (Exception $e) {
            throw new Exception("Message could not be sent. Mailer Error: {$this->mailer->ErrorInfo}");
        }
    }
}

function getEmailsFromFirestore($nextVisit) {
    $firestore = new FirestoreClient(['projectId' => 'kingaboravaccinationsystem']);
    $parentDataCollection = $firestore->collection('parentData');
    $emails = [];
    $documents = $parentDataCollection->where('NextVisit', '=', $nextVisit)->documents();

    foreach ($documents as $document) {
        if ($document->exists()) {
            $emails[] = [
                'parentEmail' => $document->data()['parentEmailAddress'],
                'childName' => $document->data()['childData']['childName'],
                'vaccineName' => $document->data()['childData']['vaccinesIssued'][0]
            ];
        }
    }
    return $emails;
}

if (isset($_GET['NextVisit'])) {
    try {
        $nextVisit = $_GET['NextVisit'];
        $emails = getEmailsFromFirestore($nextVisit);
        $mailer = new SendMail();

        foreach ($emails as $emailInfo) {
            $recipient = $emailInfo['parentEmail'];
            $childName = $emailInfo['childName'];
            $vaccineName = $emailInfo['vaccineName'];

            $subject = "Reminder: {$childName}'s Vaccination Appointment";
            $body = "<p>Dear Parent,</p>
                <p>This is a friendly reminder that your child, {$childName}, is scheduled for the {$vaccineName} vaccination on {$nextVisit}.</p>
                <p>Warm regards,<br>Kinga Bora Team</p>";

            echo $mailer->sendMail($recipient, $subject, $body) . "<br>";
        }
    } catch (Exception $e) {
        echo "Error: " . $e->getMessage();
    }
} else {
    echo "No NextVisit date provided.";
}
?>

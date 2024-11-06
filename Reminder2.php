<?php
// Include dependencies
require 'vendor/autoload.php';
require 'C:/xampp/htdocs/PHPMailer/src/PHPMailer.php';
require 'C:/xampp/htdocs/PHPMailer/src/SMTP.php';
require 'C:/xampp/htdocs/PHPMailer/src/Exception.php';

use Google\Cloud\Firestore\FirestoreClient;
use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

class VaccinationReminderService {
    private $firestore;
    private $mailer;

    public function __construct() {
        // Initialize Firestore connection
        $this->firestore = new FirestoreClient([
            'projectId' => 'kingaboravaccinationsystem' // Replace with your Firestore project ID
        ]);

        // Initialize PHPMailer
        $this->mailer = new PHPMailer(true);
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

    public function getUpcomingVaccinations($daysAhead = 14) {
        $today = new DateTime();
        $upcomingDate = (clone $today)->modify("+$daysAhead days")->format('Y-m-d');

        $parentDataCollection = $this->firestore->collection('parentData');
        $upcomingVaccinations = [];

        // Query Firestore to get parent and child data with NextVisit within the range
        foreach ($parentDataCollection->documents() as $parentDoc) {
            if ($parentDoc->exists()) {
                $parentData = $parentDoc->data();
                foreach ($parentData['childData'] as $child) {
                    if ($child['NextVisit'] == $upcomingDate) {
                        $upcomingVaccinations[] = [
                            'parentEmail' => $parentData['parentEmailAddress'],
                            'parentName' => $parentData['parentName'],
                            'childName' => $child['childName'],
                            'vaccinationName' => end($child['vaccinesIssued']),
                            'dueDate' => $child['NextVisit']
                        ];
                    }
                }
            }
        }
        return $upcomingVaccinations;
    }

    public function sendVaccinationReminders() {
        $upcomingVaccinations = $this->getUpcomingVaccinations();

        foreach ($upcomingVaccinations as $reminder) {
            $subject = "Reminder: Your Child's Vaccination is Due Soon";
            $body = "
                <p>Dear {$reminder['parentName']},</p>
                <p>This is a friendly reminder that your child, {$reminder['childName']}, is due for their {$reminder['vaccinationName']} vaccination on {$reminder['dueDate']}.</p>
                <p>Please schedule an appointment with your pediatrician as soon as possible.</p>
                <p>If you have any questions, please contact our clinic at [Clinic Phone Number].</p>
                <p>Sincerely,</p>
                <p>Kinga Bora Clinic</p>
            ";

            try {
                $this->mailer->addAddress($reminder['parentEmail']);
                $this->mailer->Subject = $subject;
                $this->mailer->Body = $body;
                $this->mailer->send();
                echo "Reminder sent to {$reminder['parentEmail']}<br>";
                $this->mailer->clearAddresses(); // Clear the address for the next email
            } catch (Exception $e) {
                echo "Error sending to {$reminder['parentEmail']}: {$e->getMessage()}<br>";
            }
        }
    }
}

// Schedule the script to send reminders
try {
    $reminderService = new VaccinationReminderService();
    $reminderService->sendVaccinationReminders();
} catch (Exception $e) {
    echo "Service error: " . $e->getMessage();
}
?>

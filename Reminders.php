<?php
// session_start();
// require 'C:/xampp/htdocs/PHPMailer/src/PHPMailer.php';
// require 'C:/xampp/htdocs/PHPMailer/src/SMTP.php';
// require 'C:/xampp/htdocs/PHPMailer/src/Exception.php';

// use PHPMailer\PHPMailer\PHPMailer;
// use PHPMailer\PHPMailer\Exception;

// class SendMail {
//     private $mailer;
    
//     public function __construct() {
//         $this->mailer = new PHPMailer(true);
        
      
//         $this->mailer->isSMTP();
//         $this->mailer->Host = 'smtp.gmail.com';
//         $this->mailer->SMTPAuth = true;
//         $this->mailer->Username = 'eoringe372@gmail.com';
//         $this->mailer->Password = 'wdjk opaf jhdx wjjr';
//         $this->mailer->SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS; 
//         $this->mailer->Port = 587;

    
//         $this->mailer->setFrom('eoringe372@gmail.com', 'KINGA BORA');
//         $this->mailer->isHTML(true); // Enable HTML
//     }
    
//     public function sendMail($recipients, $subject, $body) {
//         // Ensure recipients is an array
//         if (!is_array($recipients)) {
//             $recipients = [$recipients];
//         }
        
//         $results = [];
        
//         try {
//             foreach ($recipients as $recipient) {
//                 $this->mailer->addAddress($recipient);
//                 $this->mailer->Subject = $subject;
//                 $this->mailer->Body = $body;
                
//                 if ($this->mailer->send()) {
//                     $results[$recipient] = "Mail sent successfully";
//                 } else {
//                     $results[$recipient] = "Failed to send mail";
//                 }
                
//                 // Clear the recipient for the next loop iteration
//                 $this->mailer->clearAddresses();
//             }
//             return $results;
            
//         } catch (Exception $e) {
//             throw new Exception("Message could not be sent. Mailer Error: {$this->mailer->ErrorInfo}");
//         }
//     }
// }

// // Usage example:
// try {
//     // Instantiate SendMail class
//     $mailer = new SendMail();
    
//     $recipients = [
//         'tobikoleriari@gmail.com',
//         'peter.leriari@strathmore.edu',
//         'giftgichuhi4138@gmail.com',
//         'emmanueloringe@gmail.com'
//     ];
    
//     $subject = "Reminder: [Child Name]s Vaccination Appointment in One Week";
//     $body = "This is a friendly reminder that your child, [Child's Name], is scheduled to receive their next vaccination in one week. 

// **Vaccine Information:**
// - **Vaccine Name:** [Vaccine Name]
// - **Scheduled Date:** [Due Date]
// - **Scheduled Time:** [Due Time]
// Warm regards,  
// [Kinga Bora Team]  
// [Contact Information]  
// [Facility Address]  ";

//     $results = $mailer->sendMail($recipients, $subject, $body);
    
//     foreach ($results as $recipient => $status) {
//         echo "Recipient: $recipient - Status: $status<br>";
//     }
    
// } catch (Exception $e) {
//     echo "Error: " . $e->getMessage();
// }
// ?>

// <!-- Kangskii's function to send vaccination reminders: -->

// <?php


// class VaccinationReminderMail
// {
// public function sendVaccinationReminder($parentEmail, $childName, $childAge, $vaccineName) {
//         // Calculate the difference in weeks between today and the child's age
//         $today = new DateTime();
//         $childBirthDate = $today->sub(new DateInterval('P' . $childAge . 'Y'));
//         $interval = $today->diff($childBirthDate);
//         $weeksOld = floor($interval->days / 7);

//         // Define the reminder intervals (1 week before the due date) and messages
//         $reminders = [
//             5  => "Reminder: {$childName}'s {$vaccineName} vaccination is due in 1 week (6 weeks old).",
//             9  => "Reminder: {$childName}'s {$vaccineName} vaccination is due in 1 week (10 weeks old).",
//             13 => "Reminder: {$childName}'s {$vaccineName} vaccination is due in 1 week (14 weeks old).",
//             23 => "Reminder: {$childName}'s {$vaccineName} vaccination is due in 1 week (6 months old).",
//             27 => "Reminder: {$childName}'s {$vaccineName} vaccination is due in 1 week (7 months old).",
//             35 => "Reminder: {$childName}'s {$vaccineName} vaccination is due in 1 week (9 months old).",
//             39 => "Reminder: {$childName}'s {$vaccineName} vaccination is due in 1 week (10 months old).",
//             51 => "Reminder: {$childName}'s {$vaccineName} vaccination is due in 1 week (1 year old).",
//             63 => "Reminder: {$childName}'s {$vaccineName} vaccination is due in 1 week (15 months old).",
//             103=> "Reminder: {$childName}'s {$vaccineName} vaccination is due in 1 week (2 years old)."
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

?>
<?php
// Include Firestore and PHPMailer
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

// Usage
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
?>

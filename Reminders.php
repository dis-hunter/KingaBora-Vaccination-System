<?php
session_start();
require 'C:/xampp/htdocs/PHPMailer/src/PHPMailer.php';
require 'C:/xampp/htdocs/PHPMailer/src/SMTP.php';
require 'C:/xampp/htdocs/PHPMailer/src/Exception.php';

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
        $this->mailer->SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS; // Use STARTTLS for port 587
        $this->mailer->Port = 587;

        // Default Sender
        $this->mailer->setFrom('eoringe372@gmail.com', 'KINGA BORA');
        $this->mailer->isHTML(true); // Enable HTML
    }
    
    public function sendMail($recipients, $subject, $body) {
        // Ensure recipients is an array
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
                
                // Clear the recipient for the next loop iteration
                $this->mailer->clearAddresses();
            }
            return $results;
            
        } catch (Exception $e) {
            throw new Exception("Message could not be sent. Mailer Error: {$this->mailer->ErrorInfo}");
        }
    }
}

// Usage example:
try {
    // Instantiate SendMail class
    $mailer = new SendMail();
    
    $recipients = [
        'tobikoleriari@gmail.com',
        'peter.leriari@strathmore.edu',
        'giftgichuhi4138@gmail.com',
        'emmanueloringe@gmail.com'
    ];
    
    $subject = "KINGA BORA TEST";
    $body = "This is a test email";

    $results = $mailer->sendMail($recipients, $subject, $body);
    
    foreach ($results as $recipient => $status) {
        echo "Recipient: $recipient - Status: $status<br>";
    }
    
} catch (Exception $e) {
    echo "Error: " . $e->getMessage();
}
?>

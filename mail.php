<?php
session_start();
require 'C:\xampp\htdocs\PHPMailer\src\PHPMailer.php';
require 'C:\xampp\htdocs\PHPMailer\src\SMTP.php';
require 'C:\xampp\htdocs\PHPMailer\src\Exception.php';
// require 'C:\xampp\htdocs\PHPMailer\src\OAuth.php';
require 'vendor\autoload.php';


//Import PHPMailer classes into the global namespace
use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\SMTP;
use PHPMailer\PHPMailer\Exception;



//Load Composer's autoloader
// require 'plugins/PHPMailer/vendor/autoload.php';

//Create an instance; passing `true` enables exceptions
$mail = new PHPMailer(true);

try {
    //Server settings
    $mail->SMTPDebug = 0;                      //Enable verbose debug output
    $mail->isSMTP();                                            //Send using SMTP
    $mail->Host       = 'smtp.gmail.com';                     //Set the SMTP server to send through
    $mail->SMTPAuth   = true;                                   //Enable SMTP authentication
    $mail->Username   = 'tobikoleriari69@gmail.com';                     //SMTP username
    $mail->Password   = 'belo gjrh yrsl hyxr';                               //SMTP password
    $mail->SMTPSecure = PHPMailer::ENCRYPTION_SMTPS;            //Enable implicit TLS encryption
    $mail->Port       = 465;                                    //TCP port to connect to; use 587 if you have set 

    //Recipients
    $mail->setFrom('tobikoleriari69@gmail.com', 'Test ICS');
    $mail->addAddress('peter.leriari@strathmore.edu');     //Add a recipient

    //Content
    $mail->isHTML(true);                                  //Set email format to HTML
    $mail->Subject = 'TOBIKO OTP';
    $mail->Body    = 'Your OTP is: ' . rand(10000, 99999);

    if ($mail->send()); {
        // header("Location: otp.php");
    }



    exit;
} catch (Exception $e) {
    echo "Message could not be sent. Mailer Error: {$mail->ErrorInfo}";
}

$processForm = new SendMail();
// $processForm->SendMail();

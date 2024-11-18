<?php
//include the access token file
include 'accessToken.php';

date_default_timezone_set('Africa/Nairobi');
$processrequestUrl = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest";

// You need a live URL for callback
$callbackUrl = "https://72e9-196-200-45-130.ngrok-free.app/DarajaApi/callback.php";
$passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919";
$BusinessShortCode = "174379";
$Timestamp = date('YmdHis');

// encrypt data to get password
$password = base64_encode($BusinessShortCode . $passkey . $Timestamp);

// Get phone number and amount from POST request
$partyA = $_POST['phone']; // User's phone number
$amount = $_POST['amount']; // Amount to be paid
$partyB = $BusinessShortCode;
$AccountReference = "KINGA BORA";
$TransactionDesc = "stk push test";
$stkpushHeader = ["Content-Type:application/json", "Authorization:Bearer " . $access_token];

// INITIATE CURL
$curl = curl_init();
curl_setopt($curl, CURLOPT_URL, $processrequestUrl);
curl_setopt($curl, CURLOPT_HTTPHEADER, $stkpushHeader); // setting custom header
$curl_post_data = array(
    'BusinessShortCode' => $BusinessShortCode,
    'Password' => $password,
    'Timestamp' => $Timestamp,
    'TransactionType' => 'CustomerPayBillOnline',
    'Amount' => $amount,
    'PartyA' => $partyA,
    'PartyB' => $BusinessShortCode,
    'PhoneNumber' => $partyA,
    'CallBackURL' => $callbackUrl,
    'AccountReference' => $AccountReference,
    'TransactionDesc' => $TransactionDesc
);  
$data_string = json_encode($curl_post_data);
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
curl_setopt($curl, CURLOPT_POST, true);
curl_setopt($curl, CURLOPT_POSTFIELDS, $data_string);
$curl_response = curl_exec($curl);
// echo $curl_response;
echo "Payment request sent successfully";
?>

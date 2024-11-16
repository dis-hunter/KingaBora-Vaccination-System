<?php
header("Content-Type: application/json");
require_once 'backend\firebase.py';
use Google\Cloud\Firestore\FirestoreClient;

// Initialize Firestore
$firebase = (new FirestoreClient([
   'projectId' => 'kingaboravaccinationsystem',
   'keyFilePath' => 'backend\kingaboranewServiceKey.json'
]));

$stkCallbackResponse = file_get_contents('php://input');
$LogFile = "Mpesastkresponse.json";
$log = fopen($LogFile, "a");
fwrite($log, $stkCallbackResponse);
fclose($log);
$data = json_decode($stkCallbackResponse);
$MerchantRequestID = $data->Body->stkCallback->MerchantRequestID;
$CheckoutRequestID = $data->Body->stkCallback->CheckoutRequestID;
$resultCode = $data->Body->stkCallback->ResultCode;
$resultDesc = $data->Body->stkCallback->ResultDesc;
$Amount = $data->Body->stkCallback->CallbackMetadata->Item[0]->Value;
$MpesaReceiptNumber = $data->Body->stkCallback->CallbackMetadata->Item[1]->Value;
$UserPhoneNumber = $data->Body->stkCallback->CallbackMetadata->Item[4]->Value;

// Check if transaction is successful
if ($resultCode == 0) {
    // Store transaction details in the database
    try {
        // Prepare data for Firebase
        $transactionData = [
            "MerchantRequestID" => $MerchantRequestID,
            "CheckoutRequestID" => $CheckoutRequestID,
            "ResultCode" => $resultCode,
            "ResultDesc" => $resultDesc,
            "Amount" => $Amount,
            "MpesaReceiptNumber" => $MpesaReceiptNumber,
            "UserPhoneNumber" => $UserPhoneNumber,
            "Timestamp" => (new DateTime())->format(DateTime::ATOM), // ISO 8601 format
        ];

        // Send data to Flask API
        $url = 'http://127.0.0.1:5000/store_transaction'; // Replace with your Flask server URL if deployed
        $options = [
            'http' => [
                'header'  => "Content-type: application/json\r\n",
                'method'  => 'POST',
                'content' => json_encode($transactionData),
            ],
        ];
        $context = stream_context_create($options);
        $response = file_get_contents($url, false, $context);

        // Check if the response is successful
        if ($response === FALSE) {
            file_put_contents("callback_error.log", "Error calling Flask API" . PHP_EOL, FILE_APPEND);
            echo json_encode(["ResultCode" => 1, "ResultDesc" => "Error calling Flask API"]);
        } else {
            echo json_encode(["ResultCode" => 0, "ResultDesc" => "Transaction recorded successfully"]);
        }
    } catch (Exception $e) {
        // Handle any other errors
        file_put_contents("callback_error.log", $e->getMessage() . PHP_EOL, FILE_APPEND);
        echo json_encode(["ResultCode" => 1, "ResultDesc" => "Error processing transaction"]);
    }
} else {
    // Handle failed transaction case
    echo json_encode([
        "ResultCode" => 1,
        "ResultDesc" => "Transaction failed, ResultCode: " . $resultCode
    ]);
}
?>

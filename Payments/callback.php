<?php
header("Content-Type: application/json");
$stkCallbackResponse = file_get_contents('php://input');
$LogFile="Mpesastkresponse.json";
$log = fopen($LogFile, "a");
fwrite($log, $stkCallbackResponse);
fclose($log);
$data=json_decode($stkCallbackResponse);
$MerchantRequestID=$data->Body->stkCallback->MerchantRequestID;

$CheckoutRequestID=$data->Body->stkCallback->CheckoutRequestID;
$resultCode=$data->Body->stkCallback->ResultCode;
$resultDesc=$data->Body->stkCallback->ResultDesc;
$Amount=$data->Body->stkCallback->CallbackMetadata->Item[0]->Value;
$MpesaReceiptNumber=$data->Body->stkCallback->CallbackMetadata->Item[1]->Value;
$UserPhoneNumber=$data->Body->stkCallback->CallbackMetadata->Item[4]->Value;


//Check if transaction is successfull
if($resultCode==0){
   //Store transaction details in the database 
}

?>
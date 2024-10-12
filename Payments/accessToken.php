<?php

//Mpesa API KEYS
$consumerKey="98HXSfqDC4pwHR2zHg6y2fcAHI5BYJOTwr75QGRKAaKFFWvs";
$consumerSecret="VC0ZXrdNIDWi4EOAxn09PmQ2WwIW2hA07SMp3GG8UPsl9Vv992Ey90oqM9Vh8C5t";

//Mpesa Access Token
$access_token_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials";

$headers=["Content-Type:application/json; charset=utf8"];
$curl=curl_init($access_token_url);
curl_setopt($curl,CURLOPT_HTTPHEADER,$headers);
curl_setopt($curl,CURLOPT_RETURNTRANSFER,true);
curl_setopt($curl,CURLOPT_HEADER,false);
curl_setopt($curl,CURLOPT_USERPWD,$consumerKey.":".$consumerSecret);
$result=curl_exec($curl);
$status=curl_getinfo($curl,CURLINFO_HTTP_CODE);
$result=json_decode($result); $access_token=$result->access_token;
curl_close($curl);
?>
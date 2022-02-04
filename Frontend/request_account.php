<?php
$pubkey = $_POST["pubkey"];

$post = [
    'pubkey' => $pubkey
];

$url = "localhost:3000/get_account";

$ch = curl_init();
// Will return the response, if false it print the response
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
// Set the url
curl_setopt($ch, CURLOPT_URL,$url);
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, $post);
// Execute
$result=json_decode(curl_exec($ch), true);
// Closing
curl_close($ch);

echo $result['result'];
?>
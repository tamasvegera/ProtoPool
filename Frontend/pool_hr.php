<?php
$url = "localhost:3000/pool_data";

$ch = curl_init();
// Will return the response, if false it print the response
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
// Set the url
curl_setopt($ch, CURLOPT_URL,$url);
// Execute
$result=json_decode(curl_exec($ch), true);
// Closing
curl_close($ch);

echo $result['pool_data']['poolhash'];
?>

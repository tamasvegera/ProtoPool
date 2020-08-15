<?php
$account = $_POST["account"];

if (!filter_var($account, FILTER_VALIDATE_INT)){
	echo "Not a valid account.";
	return;
}

$url = "localhost:3000/miner_data/" . $account;

$ch = curl_init();
// Will return the response, if false it print the response
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
// Set the url
curl_setopt($ch, CURLOPT_URL,$url);
// Execute
$result=json_decode(curl_exec($ch), true);
// Closing
curl_close($ch);

$TIMESTAMP = 0;
$REWARD_BLOCK = 1;
$FROM_ACCOUNT = 2;
$AMOUNT = 3;
$PAID = 4;
$ORPHAN = 5;

// Will dump a beauty json :3
$payments = $result['miner_data']['payments'];

if (count($payments) > 0) {
    echo 'Mining statistics for the account: '.$account.'<br><br>';

	$unpaid_money = 0;
	foreach ($payments as &$payment){
		if ($payment[$PAID] == 0){
			$unpaid_money += $payment[$AMOUNT];
		}
	}
	
	echo 'Hashrate: ' . $result['miner_data']['hashrate'] .'<br>';
	echo 'Unpaid: ' . $unpaid_money . '</b><br><br>';
	
	echo '<table align="left" cellspacing="4" cellpadding="2">
	
	<tr><th>Time</th>
	<th>Block</th>
	<th>Payment account</th>
	<th>Amount</th>
	<th>Paid</th></tr>';
    foreach ($payments as $payment) {
		$time = date("Y-m-d h:i:s", $payment[$TIMESTAMP]);
		echo '<tr><td align="center">'.
		$time . '</td><td align="center">' .
		$payment[$REWARD_BLOCK] . '</td><td align="center">' .
		$payment[$FROM_ACCOUNT] . '</td><td align="center">' .
		$payment[$AMOUNT] . '</td><td align="center">';
		if ($payment[$PAID] == 1){ $paid = "Yes"; }
		elseif ($payment[$ORPHAN] == 1) { $paid = "orphan";}
		else { $paid = "No";}
		echo $paid . '</td></tr">';
    }
	echo '</table>';
} else {
    echo "No results for this account. To see statistics you need to have at least 1 valid share in 1 founded block.";
}

?>
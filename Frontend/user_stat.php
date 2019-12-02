<?php
$account = $_POST["account"];
if (!filter_var($account, FILTER_VALIDATE_INT)){
	echo "Not a valid account.";
	return;
}

$servername = "localhost";
$username = "statsite";
$password = "dicsakmorebuksi";
$dbname = "protopool";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} 

$sql = "SELECT timestamp, reward_block, from_account, amount, paid FROM protopoolpayments_v3 WHERE to_account = $account ORDER BY reward_block DESC";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    echo 'Mining statistics for the account: '.$account.'<br><br>';
	// output data of each row
	$earned_money = 0;
	$unpaid_money = 0;

	while($row = $result->fetch_assoc()) {
		$earned_money += $row['amount'];
		if ($row['paid'] == 0){
			$unpaid_money += $row['amount'];
		}
    }
	echo '<b>Earned: ' . $earned_money . '<br>';
	echo 'Unpaid: ' . $unpaid_money . '</b><br><br>';
	
	$result->data_seek(0);
	echo '<table align="left" cellspacing="4" cellpadding="2">
	
	<tr><th>Time</th>
	<th>Block</th>
	<th>Payment account</th>
	<th>Amount</th>
	<th>Paid</th></tr>';
    while($row = $result->fetch_assoc()) {
		$time = date("Y-m-d h:i:s", $row['timestamp']);
		echo '<tr><td align="center">'.
		$time . '</td><td align="center">' .
		$row['reward_block'] . '</td><td align="center">' .
		$row['from_account'] . '</td><td align="center">' .
		$row['amount'] . '</td><td align="center">';
		if ($row['paid'] == 1){ $paid = "Yes"; }
		else { $paid = "No";}
		echo $paid . '</td></tr">';
    }
	echo '</table>';
} else {
    echo "No results for this account. To see statistics you need to have at least 1 valid share in 1 founded block.";
}
$conn->close();
?>
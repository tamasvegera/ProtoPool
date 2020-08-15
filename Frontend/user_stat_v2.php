<?php
$account = 308611 #$_POST["account"];
if (!filter_var($account, FILTER_VALIDATE_INT)){
	echo "Not a valid account.";
	return;
}

$url = "localhost:3000/miner_data/308611"

$result = file_get_contents($url);
// Will dump a beauty json :3
var_dump(json_decode($result, true));

?>
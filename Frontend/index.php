
<!-- saved from url=(0025)http://pool.microcoin.hu/ -->
<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
		<title> Microcoin ProtoPool </title>
		    <meta name="viewport" content="width=device-width, initial-scale=1.0">
		<link href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" rel="stylesheet" />
<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.2.0/css/all.css" integrity="sha384-hWVjflwFxL6sNzntih27bfxkr27PmbbK/iSvJ+a4+0owXq79v+lsFkW54bOGbiDQ" crossorigin="anonymous">

		<style>
		.card {
			margin-bottom: 10px;
		}
		.container{
			margin-top: 25px;
		}
		</style>
		</head>
		<body>
		    <nav class="navbar navbar-expand-md navbar-dark bg-dark">
        <button class="navbar-toggler navbar-toggler-right" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <a href='/' class="navbar-brand">
            <img src="https://explorer.microcoin.hu/img/microcoin_webpage_logo.png" />
        </a>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav mr-auto">
                <li class="nav-item"><a class="nav-link" href="/">Mining pool</a></li>
                <li class="nav-item"><a class="nav-link" href="https://microcoin.hu">Project website</a></li>
                <li class="nav-item"><a class="nav-link" href="https://discord.gg/AmhKKcs">Discord channel</a></li>
            </ul>
        </div>
    </nav>
	
		<div class="container">
		<div class="row">
		
		<div class="col-lg-6">
		<div class="alert alert-warning">
			<div class="row"><div class="col-12">
			<b>The pool is under development, so use it only at your OWN RISK! I don't take any responsibility for any loss. You accept it by connecting to the pool. Sorry for the shitty "design".</b><br>
			For using the pool you need an account. You can request for free at Discord.
			</div></div></div>
		</div>
		<div class="col-lg-6">
			<div class="card">
			<div class="card-body"><div class="card-title">
			<h5>Check your mining stat!</h5></div>
			<form class="form" action="/user_stat_v2.php" method="post">
			<div class="form-row">
			<div class="col-10">			
				<input placeholder="Pre-dash of your account number" class="form-control" type="text" name="account">
				</div>
				<div class="col-2">
				<input class="btn btn-success" type="submit">
				</div>
				</div>
			</form>		
			</div>
			</div></div>
		</div>
		<div class="row">
		
		<div class="col-lg-12">
			
			<div class="card"><div class="card-body">			
			<div class="card-title"><h5>Parameters</h5></div>
			<table class="table table-sm" cellspacing="4" cellpadding="2">
			<tbody>
			<tr><th align="right">Pool hashrate:</th><td><?php include 'pool_hr.php';?></td></tr>
			<tr><th align="right">Pool workers:</th><td><?php include 'pool_workers.php';?></td></tr>
			<tr><th align="right">Payout:</th><td>every block after confirmation</td></tr>
			<tr><th align="right">Confirmation time:</th><td>10 blocks</td></tr>
			<tr><th align="right">Algo:</th><td>Pascal</td></tr>
			<tr><th align="right">TxFee:</th><td>0.0002 MCC</td></tr>
			<tr><th align="right">CPU, GPU, RIG (diff: 1):</th><td>pool.microcoin.hu:3333</td></tr>
			<tr><th align="right">Nicehash (diff: 32):</th><td>pool.microcoin.hu:3334</td></tr>
			<tr><th align="right">user:</th><td>pre-dash of your account number</td></tr>
			<tr><th align="right">pass:</th><td>pool fee in percentage. Valid values: 2-100. Any text or invalid value will set the fee to default 2%.</td></tr>
			</tbody></table>
			</div></div>
			</div>			
			</div>
			<div class="row"><div class="col-lg-12">
			<div class="card"><div class="card-body">			
			<div class="card-title"><h5>Claymore Dual miner example:</h5></div>
			<code>EthDcrMiner64.exe -epool eu1.ethermine.org:4444 -ewal 0x64c20f4899aa0389c35a6a64dbefe7d1ce5683e3 -epsw x -dcoin pasc -dpool stratum+tcp://pool.microcoin.hu:3333 -dwal xxxxxx -dpsw 5 -dcri 100</code><br>
			</div><div class="card-footer"><i class="fas fa-exclamation-triangle"></i> Don't forget to define the algo as Pascal as you can see in the example.</div>
			</div></div>
			<div class="col-lg-12">
			<div class="card"><div class="card-body">			
			<div class="card-title"><h5>SGminer example:</h5></div>
			 <code>sgminer -k pascal -o stratum+tcp://pool.microcoin.hu:3333 -u 1234 -p 5 -I 21 -w 64 -g 2</code>
			 </div></div>
			</div></div>
			<div class="row justify-content-md-center">
			</div>
			<div class="alert alert-success">
			<div class="row">
			
			<div class="col-12">
			<b><i class="fas fa-hand-holding-usd"></i> Donate:</b><br>
			MCC: 318291-67<br>
			BTC: 16sfNdwCJUMsKLsBHbNoNeDWee6odtkiJC
			</div></div>
		</div>
		<div class="text-center">
		<hr />
			Created by vegtamas<br>
			Frontend by Pethical<br>
			ProtoPool, 2018</div>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>		
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.bundle.min.js" integrity="sha384-pjaaA8dDz/5BgdFUPX6M/9SUZv4d12SUPF0axWc+VRZkx5xU3daN+lYb49+Ax+Tl" crossorigin="anonymous"></script>
			</body></html>

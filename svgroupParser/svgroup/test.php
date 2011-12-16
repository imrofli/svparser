<?php

try 
{
    /*** connect to SQLite database ***/

    $database = new PDO("sqlite:data.SQLITE3");

}
catch(PDOException $e)
{
    echo $e->getMessage();
    echo "<br><br>Database -- NOT -- loaded successfully .. ";
    die( "<br><br>Query Closed !!! $error");
}
$subdomain = "";
if (isset($_POST["localmensa"])) {
 	$subdomain = $_POST["localmensa"];
 	setcookie("localmensa", $subdomain, time()+60*60*24*100);
 }
else if (isset($_COOKIE["localmensa"])) {
  $subdomain = $_COOKIE["localmensa"];
  }

if ($subdomain != "" && $subdomain != "NULL") {
	echo "<br><a href=\"setmensa.php\">Mensa auswaehlen</a>";
	$day = $_GET["day"];
	if(!($day<8 and $day>-1)){
	$day=0;
	}
	
	$form = $_GET["form"];
	if($form=="xml"){
	$form_chosen=1;
	}
	else if($form=="json"){
	$form_chosen=2;
	}
	else {
	$form_chosen=0;
	}
	
	$weekmod = $_GET["weekmod"];
	if(empty($weekmod)){
	$weekmod = 0;
	}
	$mensa = escapeshellcmd($subdomain);
	if(empty($mensa) || $mensa=="NULL"){
		$mensa = "hochschule-rapperswil";
	}
	$command="python menu2xml.py " .$day ." " .$form_chosen . " " .$weekmod . " " . $mensa;
	
	if($form_chosen==1){
	header("Content-type: text/xml");
	}
	else if($form_chosen==2){
	header("Content-type: application/json; charset=UTF-8");
	}
	else {
	header("Content-type: text/html; charset=UTF-8");
	}
	//use the passthru command to execute and return the result
	
	echo passthru("$command");
	
}

else {

	header( 'Location: setmensa.php' ) ;

}

?>
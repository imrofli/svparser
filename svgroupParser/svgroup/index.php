<?php
//Fucking workaround will hostpoint kei locale frisst!!
$days = array(
    'Montag',
    'Dienstag',
    'Mittwoch',
    'Donnerstag',
    'Freitag',
    'Samstag',
    'Sonntag',
);
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
	echo "<!DOCTYPE html>";
	echo "<html>   <head>     <title>" . $subdomain . " Menuplan</title>";
	echo "     <link rel=\"icon\" type=\"image/png\" href=\"./favicon.png\">";
	echo "    <link rel=\"apple-touch-icon\" href=\"./ifavicon.png\">";
	echo "     <link href=\'http://fonts.googleapis.com/css?family=Prociono\' rel=\'stylesheet\' type=\'text/css\'>";
	echo "    <link rel=\"stylesheet\" type=\"text/css\" href=\"design.css\" >";
	echo "</head>   <body>     <div id=\"main\">";
	echo "<br><a href=\"setmensa.php\">Mensa auswaehlen</a><br>";
	$date = $_GET["date"];
	if ($date == 0){
		$today=date('d.m.Y');
	}
	else {
		$buff = strtotime($date);
		$today = date('d.m.Y', $buff);
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
	
	
	if($form_chosen==1){
	header("Content-type: text/xml");
	}
	else if($form_chosen==2){
	header("Content-type: application/json; charset=UTF-8");
	}
	else {
	header("Content-type: text/html; charset=UTF-8");
	}
	
		
	$hasValue=False;
	$query = "SELECT * FROM mensa2menu where subdomain='" . $subdomain . "'";
	if($result = $database->query($query, SQLITE_BOTH, $error))
	{
		
		while($row = $result->fetch())
	  {
	  	
	  	$strA = $row[1];
	  	if ($strA==$today){
	  	$hasValue=True;
	  	}
	  }
	}
	
	if(!$hasValue){
		$command="python menu2xml.py " .$today ." " .$form_chosen . " " . $mensa;
		passthru("$command");
		if($result = $database->query($query, SQLITE_BOTH, $error))
	{
		
		while($row = $result->fetch())
	  {
	  	
	  	$strA = $row[1];
	  	if ($strA==$today){
	  	$hasValue=True;
	  	}
	  }
	}
	}
	
	$buff = strtotime($today);
	$weekday = date('N', $buff)-1;
	if(!$hasValue){
		echo "<h1>Kein Menuplan verfuegbar</h1>";
		$query = "SELECT * FROM mensas where subdomain='" . $subdomain . "'";
		if($result = $database->query($query, SQLITE_BOTH, $error))
		{
			while($row = $result->fetch())
	  		{
	  			echo "<h2>Kontaktinformationen:</h2>"; 
	  			echo $row[1] . " / " . $row[2] . "<br>";
	  			echo $row[3] . "<br>";
	  			echo $row[4] . " " . $row[5] . "<br>";
	  			echo $row[6] . "<br>";
	  			echo "Offen:<br>" . $row[7];
	  			echo "<br><a href=\"" . $row[8] . "\">" . $row[8] . "</a>";
	  		}
		}
	}
	else {
		echo "<h1>" . $days[$weekday] ." ,". strftime('%d.%m.%Y', $buff) . "</h1>";
		$query = "SELECT * FROM menu where subdomain='" . $subdomain . "' AND date='" . $today . "'";
		if($result = $database->query($query, SQLITE_BOTH, $error))
		{
			while($row = $result->fetch())
		  {
		  	echo "<h2>" . $row[1] . "</h2>\n";
		  	echo "<p>" . $row[2];
		  	echo "<br>" . $row[3];
		  	echo "<br>" . $row[4] . " - " . $row[5] . "</p>\n";
	
		  }
		}
	}
	
}

else {

	header( 'Location: setmensa.php' ) ;

}

?>
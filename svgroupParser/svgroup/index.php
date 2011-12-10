<?php
error_reporting(EALL);
set_time_limit(60);
$day = $_GET["day"];
if(!($day<6 and $day>-1)){
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

$mensa = escapeshellcmd($_GET["mensa"]);
if(empty($mensa)){
$mensa="hochschule-rapperswil";
}
$command="python menu2xml.py " .$day ." " .$form_chosen . " " . $mensa;
//echo $command;
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
?> 
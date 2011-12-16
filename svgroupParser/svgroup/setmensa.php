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
	header("Content-type: text/html; charset=UTF-8");
	setcookie("localmensa", "", time()-3600);
		$query = "SELECT * FROM mensas";
	if($result = $database->query($query, SQLITE_BOTH, $error))
	{
	echo "<form action=\"index.php\" method=\"post\">";
	echo "<select name=\"localmensa\">\n";
	   echo "<option value=\"NULL\">Bitte Mensa auswaehlen</option>\n";
	  while($row = $result->fetch())
	  {
	  $strA = $row[9];
	      $strB = $row[1] . " / " . $row[2];
	      echo "<option value=\"$strA\">$strB</option>\n";
	  }
	  echo "</select><br>";
	  echo '<INPUT TYPE="submit" Value="Save">';
	  echo "<form>";
	}
	else {
	  die($error);
	}



?>
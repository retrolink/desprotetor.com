<?php

$link = mysql_connect("mysql.mkron.net","kronapps","nemesistk421");
if (!$link) {
    die('Could not connect: ' . mysql_error());
}

$db_selected = mysql_select_db('mkronnet_apps', $link);

// agrupar tambem por semana para olhar para o passado

$sql = "SELECT * FROM deprotect_py_success_fail ORDER BY date ASC";
$sql = "SELECT * FROM deprotect_py_success_fail where date > date_sub(now(), interval 1 month) ORDER BY date ASC";



$sth = mysql_query($sql);

$rows = array();
while($r = mysql_fetch_assoc($sth)) {
    $rows[] = $r;
}
$json = json_encode($rows);
?> 

<html>
  <head>
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['Date', 'Success', 'Failure'],
          <?
			foreach ($rows as &$value) {
			   echo "['".$value["date"]."', ".$value["success"].", ".$value["fail"]."],";

			}          	
	         ?>
        ]);

        var options = {
          title: 'Algorithm Performance'
        };

        var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
        chart.draw(data, options);
      }
    </script>
  </head>
  <body>
    <div id="chart_div" style="width: 900px; height: 500px;"></div>
  </body>
</html>



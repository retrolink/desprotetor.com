<?

echo $_SERVER['REMOTE_ADDR'];
echo "andmaytheforcebewithyou";
echo date("H");

echo md5($_SERVER['REMOTE_ADDR']."andmaytheforcebewithyou".date("H"));
?>
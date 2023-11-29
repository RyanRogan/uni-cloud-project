<?php
header("Access-Control-Allow-Origin: *");
header("Content-type: application/json");

require('functions.inc.php');

$err_msg = "Error: ";

try{
	$output = array(
		"error" => false,
		"modules" => "",
		"marks" => 0,
		"sorted_modules" => ""
	);

	$module_1 = $_REQUEST['module_1'];
	$module_2 = $_REQUEST['module_2'];
	$module_3 = $_REQUEST['module_3'];
	$module_4 = $_REQUEST['module_4'];
	$module_5 = $_REQUEST['module_5'];
	$mark_1 = $_REQUEST['mark_1'];
	$mark_2 = $_REQUEST['mark_2'];
	$mark_3 = $_REQUEST['mark_3'];
	$mark_4 = $_REQUEST['mark_4'];
	$mark_5 = $_REQUEST['mark_5'];

	$modules = array($module_1,$module_2,$module_3,$module_4,$module_5);
	$marks = array($mark_1,$mark_2,$mark_3,$mark_4,$mark_5);

	foreach($marks as $mark){
		if(!is_numeric($mark) || empty($mark)){
			$err_msg = $err_msg."All Mark Fields are required and must be numeric";
			throw new Exception(); // Throw an exception because a non-numeric character was entered as a mark
		}
	}

	foreach($modules as $module){
		if(empty($module)){
			$err_msg = $err_msg."All module fields are required";
			throw new Exception(); // Throw an exception because a non-numeric character was entered as a mark
		}
	}

	$sorted_modules=getSortedModules($modules, $marks);

	$output['modules']=$modules;
	$output['marks']=$marks;
	$output['sorted_modules']=$sorted_modules;
}
catch(Exception $e){
	// handle exception and send an error in the response
	if($err_msg != "Error: "){
		$output = array("error" => true, "error_msg" => $err_msg);
	}else{
		$output = array("error" => true, "error_msg" => "There was an unexpected error when calculating max and min marks. ".$err_msg);
	}
}

echo json_encode($output);
exit();

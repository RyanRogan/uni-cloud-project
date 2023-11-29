<?php
    require('functions.inc.php');
    use PHPUnit\Framework\TestCase;

    final class sortTest extends TestCase
    {
        public function testSortFunction(){
            $module_1 = "maths";
            $module_2 = "english";
            $module_3 = "ict";
            $module_4 = "physics";
            $module_5 = "geography";
            $mark_1 = "90";
            $mark_2 = "80";
            $mark_3 = "70";
            $mark_4 = "30";
            $mark_5 = "100";

            $modules = array($module_1,$module_2,$module_3,$module_4,$module_5);
            $marks = array($mark_1,$mark_2,$mark_3,$mark_4,$mark_5);
            
            $modules_out_expected = array(
                array("module"=>$module_5, 'marks' => $mark_5),
                array("module"=>$module_1, 'marks' => $mark_1),
                array("module"=>$module_2, 'marks' => $mark_2),
                array("module"=>$module_3, 'marks' => $mark_3),
                array("module"=>$module_4, 'marks' => $mark_4)
            );
            
            $sorted_modules=getSortedModules($modules, $marks);

            $this->assertSame($sorted_modules, $modules_out_expected);
        }
    }

?>  
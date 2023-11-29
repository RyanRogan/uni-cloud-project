    // let localProxy = "http://127.0.0.1:5004/";
    let proxyURL = "http://proxy.example.com/"; 
    let proxy2URL = "http://proxy2.example.com/";

    var proxyOnline = false;
    var proxy2Online = false;

    var global_service = "";
    var operation_gl = "";

    pingProxies(proxyURL);
    pingProxies(proxy2URL);

    const SERVICE_CLASSIFIER = "grade-classifier";
    const SERVICE_TOTAL = "grade-total";
    const SERVICE_AVERAGE = "grade-average";
    const SERVICE_REVIEW = "grade-review";
    const SERVICE_SAVE = "state-save"
    const SERVICE_SORT = "sort";
    const SERVICE_MAXMIN = "maxmin";

    module_1 = document.getElementById('module_1').value
    module_2 = document.getElementById('module_2').value
    module_3 = document.getElementById('module_3').value
    module_4 = document.getElementById('module_4').value
    module_5 = document.getElementById('module_5').value

    mark_1 = document.getElementById('mark_1').value
    mark_2 = document.getElementById('mark_2').value
    mark_3 = document.getElementById('mark_3').value
    mark_4 = document.getElementById('mark_4').value
    mark_5 = document.getElementById('mark_5').value

    function displayValueWithMsg(msg){
        document.getElementById('output-text').value = msg;
    }
    function displayServiceConError(service){
        let error_msg = "Error: Cannot connect to service '" + service + "'";
        document.getElementById('output-text').value = error_msg;
    }
    
    function displayServiceError(error){
        let error_msg = "Error: " + error;
        document.getElementById('output-text').value = error_msg;
    }
    
    function displayLoadMsg(){
        document.getElementById('output-text').value = "Calculating...";
    }
    

    function updateInputs(){
        displayLoadMsg();

        module_1 = document.getElementById('module_1').value
        module_2 = document.getElementById('module_2').value
        module_3 = document.getElementById('module_3').value
        module_4 = document.getElementById('module_4').value
        module_5 = document.getElementById('module_5').value

        mark_1 = document.getElementById('mark_1').value
        mark_2 = document.getElementById('mark_2').value
        mark_3 = document.getElementById('mark_3').value
        mark_4 = document.getElementById('mark_4').value
        mark_5 = document.getElementById('mark_5').value
    }
    function pingProxies(url){
        let xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.status == 200 && this.readyState == 4 ) {
                if (url == proxyURL){
                    proxyOnline = true;
                }else if (url == proxy2URL){
                    proxy2Online = true;
                }
            }else{
                if (url == proxyURL){
                    proxyOnline = false;
                }else if (url == proxy2URL){
                    proxy2Online = false;
                }
            }
        };
        xhttp.open("GET", url);
        xhttp.send();
    }
    function determineProxy(){
        if (proxyOnline){
            console.log("Proxy 1 Online and being used");
            return proxyURL;
        }else if (proxy2Online){
            console.log("Proxy 2 Online and being used");
            return proxy2URL;
        }else{
            return false;
        }
    }
    function getProxyUrl(service){
        try{
            proxy_url = determineProxy()
            if(proxy_url == false){
                displayServiceError("Cannot connect to any services")
                return;
            }
            if(service != SERVICE_SAVE){
                global_service = service;
            }else{
                if(operation_gl != "add"){
                    return proxy_url+"?service=" + service;
                }
            }
            return proxy_url+"?service=" + service + "&module_1=" + module_1 + "&mark_1=" + mark_1 + "&module_2=" + module_2 + "&mark_2=" + mark_2
            + "&module_3=" + module_3 + "&mark_3=" + mark_3 + "&module_4=" + module_4 + "&mark_4=" + mark_4
            + "&module_5=" + module_5 + "&mark_5=" + mark_5;
        }catch(err){
            console.log("Cannot connect to any services");
            displayServiceError("Cannot connect to any services")
            return;
        }
    }
    function validateInputs(){
        let isValid = true;
        mark_inputs = [mark_1, mark_2, mark_3, mark_4, mark_5];
        module_inputs = [module_1, module_2, module_3, module_4, module_5];

        for(let i = 0; i < mark_inputs.length; i++){
            item = mark_inputs[i];
            if(isNaN(item)){
                displayValueWithMsg("Error: Mark " + (i+1) + " is invalid");
                isValid = false;
            }else if(item.trim() == ""){
                displayValueWithMsg("Error: Mark " + (i+1) + " is a required field");
                isValid = false;
            }else if(item < 0 || item > 100){
                displayValueWithMsg("Error: Mark " + (i+1) + " must be within 0 and 100");
                isValid = false;
            }
            
            if(!isValid){
                return isValid;
            }
        }
        
        if(isValid){
            for(let i = 0; i < module_inputs.length; i++){
                item = module_inputs[i];
                if(item.trim() == ""){
                    displayValueWithMsg("Error: Module " + (i+1) + " is a required field");
                    return false;
                }
            }
        }
        return true;
    }

    function clearText()
    {
        document.getElementById('module_1').value = '';
        document.getElementById('module_2').value = '';
        document.getElementById('module_3').value = '';
        document.getElementById('module_4').value = '';
        document.getElementById('module_5').value = '';

        document.getElementById('mark_1').value = '';
        document.getElementById('mark_2').value = '';
        document.getElementById('mark_3').value = '';
        document.getElementById('mark_4').value = '';
        document.getElementById('mark_5').value = '';

        document.getElementById('output-text').value = '';
    }

    function getMaxMin()
    {
        updateInputs();

        if(validateInputs()){
            let xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    var j = JSON.parse(this.response);

                    if(j.hasOwnProperty('error_msg')){
                        displayServiceError(j.error_msg)
                    }else{
                        let max_module = j.max_module;
                        let min_module = j.min_module;
                        displayValueWithMsg('Highest scoring module = ' + max_module
                                        + '\nLowest scoring module = ' + min_module);
                    }
                }else if (this.readyState == 4 && this.status != 200){
                    displayServiceConError("Highest & Lowest Scoring Modules");
                }
            };
            xhttp.open("GET", getProxyUrl(SERVICE_MAXMIN));
            xhttp.send();
            return;
        }
    }

    function getSortedModules()
    {
        updateInputs();

        if(validateInputs()){
            let xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    var j = JSON.parse(this.response);
                    
                    if(j.hasOwnProperty('error_msg')){
                        displayServiceError(j.error_msg)
                    }else{
                        let sorted_modules_returned = j.sorted_modules;
                        let sorted_modules = '';
                        for (let i = 0; i < sorted_modules_returned.length; i++) {
                            sorted_modules += sorted_modules_returned[i]['module'] + ' - ' + sorted_modules_returned[i]['marks'] + '\r\n';
                        }
                        displayValueWithMsg(sorted_modules);
                    }
                }else if (this.readyState == 4 && this.status != 200){
                    displayServiceConError("Sort Marks");
                }
            };
            xhttp.open("GET", getProxyUrl(SERVICE_SORT));
            xhttp.send();
            return;
        }
    }

    function getTotal()
    {
        updateInputs();

        if(validateInputs()){
            let xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    var j = JSON.parse(this.response);
                    
                    if(j.hasOwnProperty('error_msg')){
                        displayServiceError(j.error_msg)
                    }else{
                        let total_marks = j.total_marks;
                        displayValueWithMsg('Total Marks = ' + total_marks);
                    }
                }else if (this.readyState == 4 && this.status != 200){
                    displayServiceConError("Total Marks");
                }
            };

            xhttp.open("GET", getProxyUrl(SERVICE_TOTAL));

            xhttp.send();
            return;
        }
    }

    function getClassification()
    {
        updateInputs();
        
        if(validateInputs()){
            let xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    var j = JSON.parse(this.response);

                    if(j.hasOwnProperty('error_msg')){
                        displayServiceError(j.error_msg)
                    }else{
                        let grade_msg = "Overall Grade = " + j.overall_grade + "\n\n" + 
                        module_1 + " = " + j.grade_1 + "\n" +
                        module_2 + " = " + j.grade_2 + "\n" + 
                        module_3 + " = " + j.grade_3 + "\n" +
                        module_4 + " = " + j.grade_4 + "\n" +
                        module_5 + " = " + j.grade_5 ;
                        displayValueWithMsg('Grade Classifications\n' + grade_msg);
                    }
                }else if (this.readyState == 4 && this.status != 200){
                    displayServiceConError("Grade Classification");
                }
            };
            xhttp.open("GET", getProxyUrl(SERVICE_CLASSIFIER));
            xhttp.send();
            return;
        }
    }

    function getAverage()
    {
        updateInputs();

        if(validateInputs()){
            let xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    var j = JSON.parse(this.response);
                    
                    if(j.hasOwnProperty('error_msg')){
                        displayServiceError(j.error_msg)
                    }else if(j.hasOwnProperty('error')){
                        displayValueWithMsg("Error: " + j.error)
                    }else{
                        let average_mark = j.average_mark;
                        displayValueWithMsg("The average mark is: " + average_mark);
                    }
                }else if (this.readyState == 4 && this.status != 200){
                    displayServiceConError("Average Mark");
                }
            };
            xhttp.open("GET", getProxyUrl(SERVICE_AVERAGE));
            xhttp.send();
            return;
        }
    }

    function gradeReviewMSg(module, mark){
        return module + " - " + mark + " extra marks";
    }
    function getGradeReview()
    {
        updateInputs();
        
        if(validateInputs()){
            let xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    var j = JSON.parse(this.response);

                    if(j.hasOwnProperty('error_msg')){
                        displayServiceError(j.error_msg)
                    }else if(j.hasOwnProperty('error')){
                        displayValueWithMsg("Error: " + j.error)
                    }else{
                        let grade_review = "To achieve the next grade, you need:\n\n" + 
                        gradeReviewMSg(module_1, j.grade_1) + "\n" + 
                        gradeReviewMSg(module_2, j.grade_2) + "\n" + 
                        gradeReviewMSg(module_3, j.grade_3) + "\n" + 
                        gradeReviewMSg(module_4, j.grade_4) + "\n" + 
                        gradeReviewMSg(module_5, j.grade_5) + "\n";

                        displayValueWithMsg(grade_review);
                    }
                }else if (this.readyState == 4 && this.status != 200){
                    displayServiceConError("Grade Review");
                }
            };
            xhttp.open("GET", getProxyUrl(SERVICE_REVIEW));
            xhttp.send();
            return;
        }
    }
    function saveRequest(){
        stateSaver("add");
    }
    function retreiveRequest(){
        stateSaver("get");
    }
    function deleteRequest(){
        stateSaver("delete");
    }
    function stateSaver(operation){
        operation_gl = operation;
        // Don't need to update inputs since we are using the inputs for the most recent transaction. 
        // We do need to still validate the data to make sure it's still valid as there's no point in saving an invalid request
        // updateInputs(); 
        let record_id = document.getElementById("save_id").value;
        if (!isIdValid(record_id)){
            showSaveError("ID is a required field");
            return;
        }
        else if(operation == "add" && !validateInputs()){
            return;
        }
        else{
            let xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    var j = JSON.parse(this.response);
                    
                    if(j.hasOwnProperty('error_msg')){
                        showSaveError(j.error_msg)
                    }else{
                        if(operation == "get"){
                            let output = j.output;
                            let service = j.service;
                            output.replace('[break]','\n');
                            // Display in Output Box
                            displayValueWithMsg(output);
                            // Display Individual Textboxes
                            displayInElement("module_1", j.modules.module_1);
                            displayInElement("module_2", j.modules.module_2);
                            displayInElement("module_3", j.modules.module_3);
                            displayInElement("module_4", j.modules.module_4);
                            displayInElement("module_5", j.modules.module_5);
                            displayInElement("mark_1", j.marks.mark_1);
                            displayInElement("mark_2", j.marks.mark_2);
                            displayInElement("mark_3", j.marks.mark_3);
                            displayInElement("mark_4", j.marks.mark_4);
                            displayInElement("mark_5", j.marks.mark_5);
                            showSaveSuccess("Successfully retrieved data for ID '" + record_id + "'")
                        }else{
                            showSaveSuccess(j.success_msg)
                        }
                    }
                }else if (this.readyState == 4 && this.status != 200){
                    showSaveError("Error: Problem Connecting to DB");
                }
            };
            let save_url = getProxyUrl(SERVICE_SAVE)+ "&id="+record_id+"&option="+operation
            if(operation == "add"){
                let output_box = document.getElementById("output-text").value;
                save_url = save_url +"&out_service="+global_service+"&output="+output_box;
            }
            xhttp.open("GET", save_url);
            xhttp.send();
            return;
        }
    }
    function isIdValid(id){
        return !id.trim() == "";
    }
    function displayInElement(id, msg){
        document.getElementById(id).value = msg;
    }
    function setupApp(){
        const error_msg = document.getElementById("error_msg");
        const success_msg = document.getElementById("success_msg");

        error_msg.style.display = "none";
        success_msg.style.display = "none";
    }
    function showSaveError(msg){
        error_msg.style.display = "initial";
        success_msg.style.display = "none";

        error_msg.innerText = msg;
    }
    function showSaveSuccess(msg){
        error_msg.style.display = "none";
        success_msg.style.display = "initial";

        success_msg.innerText = msg;
    }
    setupApp();
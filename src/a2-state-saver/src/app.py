from flask import Flask, request, Response, render_template
import json
from SaveStateException import SaveStateException
import saving_utils as su

app = Flask(__name__)
su.setFile()
# Global Variable
ERROR_MSG_KEY = "error_msg"
SUCCESS_MSG_KEY = "success_msg"

# JSON file takes the form ID => {service => '', modules => {1=>'',2=>'',3=>'',4=>'',5=>''}, marks => {1=>'',2=>'',3=>'',4=>'',5=>''}, output_txt=>''}
def responseBuilder(reply):
    res = Response(json.dumps(reply))
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Content-type:'] = 'application/json'
    return res

@app.route("/add")
def index():
    try:
        data = {        
            "modules": {
                "module_1": "",
                "module_2": "",
                "module_3": "",
                "module_4": "",
                "module_5": ""
            },
            "marks": {
                "mark_1": "",
                "mark_2": "",
                "mark_3": "",
                "mark_4": "",
                "mark_5": ""
            },
            "output": request.args.get("output"),
            "service": request.args.get("service")
        }
        id = request.args.get("id")
        is_id_valid = su.idValidation(id)
        if id == None:
            raise SaveStateException("ID cannot be null")
        elif not is_id_valid['result']:
            raise SaveStateException(is_id_valid['reason'])
        
        mod_key_lst = list(data['modules'].keys())
        mark_key_lst = list(data['marks'].keys())
        for i in range(len(mod_key_lst)):
            mo_k = mod_key_lst[i]   # get module key
            ma_k = mark_key_lst[i]  # get mark key
            data['modules'][mo_k] = request.args.get(mo_k)  # populating modules
            data['marks'][ma_k] = request.args.get(ma_k)    # populating marks
            # Validate Modules and Marks
            if data['modules'][mo_k] == None:
                raise SaveStateException(mo_k + " is a required field")
            if data['marks'][ma_k] == None:
                raise SaveStateException(ma_k + " is a required field")

        res = su.addToFile(id,data)

        if res:
            display_message = {"id": id, SUCCESS_MSG_KEY:"Data added successfully"}
        else:
            raise SaveStateException("Cannot add record as ID (" + id + ") already exists")
    except SaveStateException as ex:
        print("SaveStateException:\n",ex)
        display_message = {ERROR_MSG_KEY: str(ex.args[0])}
    except Exception as ex:
        print("Exception:\n",ex)
        display_message = {ERROR_MSG_KEY: "Error: An unexpected error has occurred"}

    return responseBuilder(display_message)

@app.route("/get/all_records")
def get_all_records():
    try:
        reply = su.readFile()
    except SaveStateException as ex:
        print("SaveStateException:\n",ex)
        reply = {ERROR_MSG_KEY: str(ex.args[0])}
    except Exception as ex:
        print("Exception:\n",ex)
        reply = {ERROR_MSG_KEY: "Error: An unexpected error has occurred"}

    return responseBuilder(reply)

@app.route("/get/record/<id>")
def get_record_by_id(id):
    try:
        record = su.getRecord(id)
        if record == -1:
            raise SaveStateException(f"Error: record with ID '{id}' doesn't exist")
        reply = record
    except SaveStateException as ex:
        print("SaveStateException:\n",ex)
        reply = {ERROR_MSG_KEY: str(ex.args[0])}
    except Exception as ex:
        print("Exception:\n",ex)
        reply = {ERROR_MSG_KEY: "Error: An unexpected error has occurred"}
    return responseBuilder(reply)

@app.route("/delete/record/<id>")
def delete_record_id(id):
    try:
        deletion = su.deleteRecord(id)
        if deletion:
            return {SUCCESS_MSG_KEY: f"Record {id} deleted"}
        else:
            raise SaveStateException(f"Record {id} could not be deleted")
    except SaveStateException as ex:
        print("SaveStateException:\n",ex)
        reply = {ERROR_MSG_KEY: str(ex.args[0])}
    except Exception as ex:
        print("Exception:\n",ex)
        reply = {ERROR_MSG_KEY: "Error: An unexpected error has occurred"}
    return responseBuilder(reply)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006)

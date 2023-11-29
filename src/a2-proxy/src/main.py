from flask import Flask, request, Response
import json, requests
from proxy_utils import *

app = Flask(__name__)

urls = load_url_config()

@app.route("/", methods=['GET'])
def index_page():
    print()
    service = ""
    try:
        # Get the service name
        service = request.args.get('service')
        urli = get_url(service, urls)
        # if service in urls:
        if not urli == -1:
            # Get the Marks
            mark_1 = request.args.get('mark_1')
            mark_2 = request.args.get('mark_2')
            mark_3 = request.args.get('mark_3')
            mark_4 = request.args.get('mark_4')
            mark_5 = request.args.get('mark_5')
            # Get the Modules
            module_1 = request.args.get('module_1')
            module_2 = request.args.get('module_2')
            module_3 = request.args.get('module_3')
            module_4 = request.args.get('module_4')
            module_5 = request.args.get('module_5')
            
            request_data = {
                "mark_1" : mark_1,
                "mark_2" : mark_2,
                "mark_3" : mark_3,
                "mark_4" : mark_4,
                "mark_5" : mark_5,
                "module_1" : module_1,
                "module_2" : module_2,
                "module_3" : module_3,
                "module_4" : module_4,
                "module_5" : module_5
            }
            get_request = f"?mark_1={mark_1}&mark_2={mark_2}&mark_3={mark_3}&mark_4={mark_4}&mark_5={mark_5}&module_1={module_1}&module_2={module_2}&module_3={module_3}&module_4={module_4}&module_5={module_5}"
            # url = urls[service]
            if service == "state-save":
                print("Entered service")
                option = request.args.get('option')                
                id = request.args.get('id')
                output = request.args.get('output')
                srvc = request.args.get('out_service')
                # Validation
                if option == "add" and not srvc in urls or not option in urls[service]:
                    raise Exception("Service or Option does not exist")
                if option == "add":
                    get_request += f"&id={id}&service={srvc}&output={output}"
                else:
                    get_request = id
                # Generate Url
                urli = get_saver_url(option, urli) + get_request

            print(f"Sending Request to {urli} with data \n{get_request}")
            resp = requests.get(url = urli, params=request_data)
            resp_data = json.dumps(resp.json())
        else:
            resp_data = json.dumps({"error_msg" : f"Service '{service}' is invalid"})
    except Exception as ex:
        print("Exception Caught:", ex)
        resp_data = json.dumps({"error_msg" : "An error occurred when contacting the service "+service})

    print("Response ", resp_data)
    res = Response(resp_data)
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Content-type:'] = 'application/json'
    return res

@app.route("/health", methods=['GET'])
def health_page():
    return {"status": "online"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
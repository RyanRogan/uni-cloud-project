from flask import Flask, request, Response, render_template, session, redirect
import json
from my_log import myLog
import admin_config as ac

app = Flask(__name__)
app.secret_key = "this_is_secret"

ml = myLog("Web App")
STATS_URI = "configs/service-stats.json"

# CONSTANTS
UNEXPECTED_ERROR_MSG={"error_msg" : "An unexpected error occurred"}

def getStats():
    stats = {}
    try:
        with open(STATS_URI) as serivce_stats_file:
            stats = json.load(serivce_stats_file)
        ml.log_info("Stats Successfully Retreived")
    except Exception as e:
        ml.log_error("Exception Detected when getting stats\n"+str(e))
        stats = {}
    return stats

def responseBuilder(reply):
    ml.log_info("Building Response")
    res = Response(json.dumps(reply))
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Content-type:'] = 'application/json'
    return res

@app.route("/", methods=['GET', 'POST'])
def index_page():
    stats = getStats()
    return render_template('./index.html', stats=stats)

@app.route("/getStats")
def get_stats_page():
    try:
        reply = getStats()
    except Exception:
        reply = UNEXPECTED_ERROR_MSG
    return responseBuilder(reply)

@app.route("/check/proxies")
def get_proxy():
    try:
        ml.log_info("Getting proxy status")
        stats = getStats()
        if stats['proxy']['healthy'] == True:
            reply = {"proxy": "proxy"}
        elif stats['proxy2']['healthy'] == True:
            reply = {"proxy": "proxy2"}
        else:
            reply = {"error_msg" : "There are no proxies online"}
    except Exception:
        reply = UNEXPECTED_ERROR_MSG
    if "error_msg" in reply:
        ml.log_error("There was an issue with getting the proxy status. Reason: " + reply["error_msg"])
    else:
        ml.log_info("A healthy proxy has been found. The proxy we'll be using is '"+reply["proxy"]+"'")
    return responseBuilder(reply)

@app.route("/get/<service>")
def get_service(service):
    try:
        stats = getStats()
        if service in stats:
            reply = stats[service]
        else:
            reply = {"error_msg" : "Service does not exist"}
    except Exception:
        reply = UNEXPECTED_ERROR_MSG
    if "error_msg" in reply:
        ml.log_error("Could not retrieve stats for service '"+service+"'. Reason: " + reply["error_msg"])
    else:
        ml.log_info("Service stats found for '"+service+"'")
    return responseBuilder(reply)

@app.route("/admin", methods=['GET', 'POST'])
def admin_panel():
    page_data = {'sign_in': False}
    if 'username' in session:
        username = session['username']
        log_conts = []
        for x in ml.readLogFile():
            log_conts.append(x)
        page_data['sign_in'] = True
        page_data['logs'] = log_conts #.readline()
        admin_c = ac.readConfig()
        page_data['admin'] = admin_c
    elif 'error' in session:
        page_data['error'] = session['error']
        session.pop('error', None)

    return render_template('./admin.html', data=page_data)

@app.route("/login", methods=['POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == "admin" and request.form['password'] == "password":
            session['username'] = "admin"
        else:
            session['error'] = "Incorrect Username or Password"
    return redirect("/admin")

@app.route("/logout", methods=['GET','POST'])
def logout():
    if 'username' in session:
      session.pop('username', None)
    return redirect("/admin")

@app.route("/monitor-update", methods=['GET','POST'])
def admin_update():
    if request.method == 'POST':
        if 'username' in session:
            freq = request.form['freq']
            if int(freq) >= 15:
                toggle = True
                if not 'toggle' in request.form:
                    toggle = False
                admin_data = ac.readConfig() # Set Config Data
                admin_data['monitor'] = toggle
                admin_data['frequency'] = freq
                ac.writeConfig(admin_data) # Write to Config File
            else:
                ml.log_error("Frequency needs to be greater than or equal to 15")
    return redirect("/admin")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)
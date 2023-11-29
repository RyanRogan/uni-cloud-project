from my_log import myLog
import requests, json
import time
from os import system
import email_test as em
import admin_config as ac

ml = myLog("monitor")
STATS_URI = "configs/service-stats.json"
# Functions - Start
# Healthcheck Function - Checks that the server is up
def health_check(service, res):
    if res.status_code == 200:
        ml.log_info(f"Service {service} is healthy")
        return True
    else:
        ml.log_error(f"Cannot connect to service {service}") 
        return False

correctness_vals = {'grade-total': {"total_marks": "450"}, 
                    'maxmin': {"error":False,"modules":["maths","ICT","Science","Geography","English"],"marks":["90","90","90","90","90"],"max_module":"maths - 90","min_module":"English - 90"}, 
                    'sort': {"error":False,"modules":["maths","ICT","Science","Geography","English"],"marks":["90","90","90","90","90"],"sorted_modules":[{"module":"maths","marks":"90"},{"module":"ICT","marks":"90"},{"module":"Science","marks":"90"},{"module":"Geography","marks":"90"},{"module":"English","marks":"90"}]}, 
                    'grade-classifier': {"grade_1":"Distinction","grade_2":"Distinction","grade_3":"Distinction","grade_4":"Distinction","grade_5":"Distinction","overall_grade":"Distinction"}, 
                    'grade-average': {"average_mark":"90.0"}, 
                    'grade-review': {"grade_1":"0.0","grade_2":"0.0","grade_3":"0.0","grade_4":"0.0","grade_5":"0.0"},
                    "proxy" : {"status": "online"},
                    "proxy2": {"status": "online"}
                    }
# Correctness Check Function - Checks that the response matches the expected response
def correctness_check(service, res):
    ml.log_info("Checking for Correctness with service " + service)
    res_t = res.json()
    ret = False
    if service in correctness_vals:
        ml.log_info(f"{service} is valid")
        if res_t == correctness_vals[service]:
            ml.log_info(f"{service} returns correct response based on test data")
            ret = True
        else:
            ml.log_error(f"{service} returns incorrect response based on test data\nActual:\n{res_t}\n\nExpected:\n{str(correctness_vals[service])}")
    else:
        ml.log_error(f"{service} is not in test data. It could be invalid or the tests for this service could be missing")
    return ret
def getStats():
    ml.log_info("Found stats: "+service_stats)
    return service_stats
def getServiceStats(service):
    if service in service_stats:
        return service_stats[service]
    else:
        return -1

urls = {
    "grade-total": "http://grade-total.example.com/",
    "maxmin": "http://grade-maxmin.example.com/",
    "sort" : "http://grade-sort.example.com/",
    "grade-classifier" : "http://grade-classifier.example.com",
    "grade-average" : "http://grade-average.example.com/",
    "grade-review" : "http://grade-review.example.com/",
    "proxy" : "http://proxy.example.com/health",
    "proxy2": "http://proxy2.example.com/health"
}
# proxy_url = "http://proxy.example.com/"

# Get the Marks
mark_1 = "90"
mark_2 = "90"
mark_3 = "90"
mark_4 = "90"
mark_5 = "90"
# Get the Modules
module_1 = "maths"
module_2 = "ICT"
module_3 = "Science"
module_4 = "Geography"
module_5 = "English"

get_request = f"?mark_1={mark_1}&mark_2={mark_2}&mark_3={mark_3}&mark_4={mark_4}&mark_5={mark_5}&module_1={module_1}&module_2={module_2}&module_3={module_3}&module_4={module_4}&module_5={module_5}"

def readContents():
    json_stats = {}
    try:
        with open(STATS_URI, "r") as sfile:
            json_stats = json.load(sfile)
    except Exception:
        ml.log_error("Stat File could not be read. Assuming it's empty so using an empty dictionary instead")
    return json_stats

service_stats = readContents()
def monitor():
    ml.log_info("Application Started")
    while True:
        admin_c = ac.readConfig()
        if admin_c['monitor']:
            for k,v in urls.items():
                try:
                    fields = ['healthy', 'correct', 'time']
                    if not k in service_stats:
                        ml.log_warn("Stats for service '"+k+"' do not exist. We need to construct them now.")
                        service_stats[k] = {}
                        for i in fields:
                            ml.log_info("Adding Field: "+i)
                            service_stats[k][i] = ""
                    stat_obj = service_stats[k]
                    if k == "proxy" or k == "proxy2":
                        url = v
                    else:
                        url = v + get_request
                    # Perform test on service
                    ml.log_info("Pinging " + url)
                    res = requests.get(url)  # Sending Request
                    hc = health_check(k, res) # Performing Health Check
                    cc = False
                    if hc: # Only check correctness if server is up
                        cc = correctness_check(k, res) # Check Correctness
                    # Checking Stats for any new issues
                    error = False
                    if stat_obj['healthy'] == True and hc == False:
                        ml.log_error(f"{k} is no longer healthy")
                        error = True
                    elif stat_obj['correct'] == True and cc == False:
                        ml.log_error(f"{k} is no longer correct")
                        error = True
                    # Record Stats
                    stat_obj['time'] = float(res.elapsed.total_seconds()) # Recording response time
                    stat_obj['last_updated'] = ml.get_current_dt() # Recording the date and time of this update
                    stat_obj['healthy'] = hc
                    stat_obj['correct'] = cc
                    if error:
                        em.make_email(k,stat_obj)
                except Exception as e:
                    ml.log_error("An unexpected error has occured\n" + str(e) + "\n")
                print() # Line Break
            # Perform File operations to enter the current stats
            ml.log_info("Opened File")
            stat_file = open(STATS_URI, "w+")
            stat_file.write(str(json.dumps(service_stats)))
            stat_file.close()
            ml.log_info("Closed File")
            em.send_error()
        else:
            ml.log_info("Monitor is switched Off by Admin")
        # Sleep for 30 seconds to avoid the server rejecting the request
        wait_freq = int(admin_c['frequency'])
        ml.log_info("Waiting for " + str(wait_freq) + " seconds")
        time.sleep(wait_freq)
monitor()
from flask import Flask, request, Response
import json

app = Flask(__name__)

def getTotal(lst):
    total = 0
    if len(lst) == 0:
        return 0
    for i in range(len(lst)):
        total = total + int(lst[i])
    return total

@app.route("/", methods=['GET', 'POST'])
def index_page():
    try:
        mark_1 = request.args.get('mark_1')
        mark_2 = request.args.get('mark_2')
        mark_3 = request.args.get('mark_3')
        mark_4 = request.args.get('mark_4')
        mark_5 = request.args.get('mark_5')

        marks = [int(mark_1), int(mark_2), int(mark_3), int(mark_4), int(mark_5)]
        total_res = json.dumps({"total_marks" : str(getTotal(marks))})    
    except Exception as ex:
        print("Exception Caught:", ex)
        total_res = json.dumps({"error_msg" : "An error occurred when performing Total Calculation"})

    res = Response(total_res)
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Content-type:'] = 'application/json'
    
    return res

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
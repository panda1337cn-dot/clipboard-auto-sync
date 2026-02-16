import flask
from flask import Flask
from flask import request
import time
app = Flask(__name__)
pushed = {}
clip_cloud_data=""
@app.route("/update/<machine_id>")
def update(machine_id,**args):
    global pushed,clip_cloud_data,update_time
    update_time = time.time()
    data = request.form.get("data")
    print(data)
    clip_cloud_data = data
    pushed={}
    pushed[machine_id] = True
    return "ok"

@app.route("/update_status/<machine_id>")
def update_status(machine_id):
    global pushed
    pushed[machine_id] = True
    return "ok"
@app.route("/check/<machine_id>")
def check(machine_id):
    if pushed.get(machine_id,False) == False:
        return "0"
    return "1"

@app.route("/get_content/<machine_id>")
def get_content(machine_id):
    global pushed
    pushed[machine_id] = True
    return clip_cloud_data

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=5000)

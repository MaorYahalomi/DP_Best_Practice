#from Flask_Project.DP_Portal.error_handling import Error_handler
from flask import render_template
from flask import request
import json
from portal import app
from vision import Vision
from error_handling import Error_handler

@app.route('/')
@app.route('/index.html')
def index():
    user = {'username': 'Maory'}
    return render_template('index.html', title='Home', user=user)

@app.route('/maor')
def maor():
    user = {'username': 'Maor'}
    return render_template('maor.html')

@app.route('/login',methods=['POST'])
def login():
    try:          
        vision_ip = request.form["vision"]
        vision_user = request.form["username"]
        vision_pass = request.form["password"]
        v1 = Vision(vision_ip, vision_user, vision_pass )
        v1.login()
    except Error_handler as e:
        return {"status":"error", "msg":e.message}

    return {"status":"success"}
    #return "success"
    
@app.route('/login.html',methods=['GET'])
def login_input_page():
    return render_template('login.html')

@app.route('/config.html',methods=['GET'])
def config():
    return render_template('dpconfig.html')
# Main server app
from user.models import User
import base64
import json
import os
from os.path import join, dirname, realpath, basename
from model.match import compare_func
import requests
from flask import Flask, render_template, request, redirect, url_for, make_response, session
from werkzeug.utils import secure_filename
from flask import flash
from io import BytesIO
from PIL import Image
import numpy as np

import database

os.chdir(__file__.replace(basename(__file__), ''))

app = Flask(__name__)
UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/uploads/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


DB_URL = "mongodb+srv://manish05:manish05@cluster0.z3buhby.mongodb.net/?retryWrites=true&w=majority"

@app.route('/')
def index():
    if "username" in session:
        return render_template("login.html")
    else:
        return redirect('/logout')
    # return render_template("intro.html")


@app.route('/register', methods=['POST', 'GET'])
def register():
    # Handles a user signup
    if (request.method == 'POST'):
        user = User()
        success_flag = user.signup()
        if (success_flag):
            flash('Your account was created succesfully!', "success")
            return redirect('/login')
        else:
            flash('User email already in use.', "error")
            return redirect('/register')

            # Default GET route
    return render_template('register.html')


@app.route('/logout')
def logout():
    # handles a user logout
    try:
        user = User()
        success_flag = user.logout()
        if success_flag:
            flash('You were logged out succesfully!', "success")
            return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))
    except:
        flash("You are not logged in", "warning")
        return redirect(url_for('login'))

@app.route('/adminpage')
def adminpage():
    case = database.source("all_cases.sql")
    case_dict = {c[0]: c[1] + " " + c[2] for c in case}

    detective = database.source("all_detective.sql")

    return render_template("index.html",
                           case=case, len_case=len(case),
                           detective=detective,
                           len_det=len(detective),
                           case_dict=case_dict)

@app.route('/detectivepage/<did>', methods=['GET', 'POST'])
def detectivepage(did):
    # did = request.args["did"]
    case = database.source("selected_cases.sql", did)
    case_dict = {c[0]: c[1] + " " + c[2] for c in case}

    detective = database.source("all_detective.sql")

    return render_template("detectivepage.html",
                           case=case, len_case=len(case),
                           detective=detective,
                           len_det=len(detective),
                           case_dict=case_dict)

@app.route('/Uploadimage', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        case_id = request.form['case_id']
        # Set up the ImgBB API key and endpoint URL
        imgbb_api_key = "cb21bdae432dcb24b3a28484be9dcd60"
        imgbb_url = "https://api.imgbb.com/1/upload?key=" + imgbb_api_key

        # Get the uploaded image file and other parameters
        image_file = request.files['image']
        image_data = image_file.read()
        image_name = image_file.filename
        # print(image_name)
        # with open("static/assets/b1.jpg","rb") as image_file:
        #     image_data = image_file.read()
        #     image_name = "b2.jpg"

        # Encode the image data in base64
        image_data_base64 = base64.b64encode(image_data)

        # Set up the ImgBB API request
        imgbb_data = {
            "image": image_data_base64.decode(),
            "name": image_name
        }
        imgbb_response = requests.post(imgbb_url, data=imgbb_data)

        # Extract the image URL from the ImgBB API response
        imgbb_json = json.loads(imgbb_response.content)
        imgbb_url = imgbb_json["data"]["url"]
        # Store the image URL in the SQL database
        # mycursor = mydb.cursor()
        # sql = "INSERT INTO images (url) VALUES (%s)"
        # val = (imgbb_url,)
        # mycursor.execute(sql, val)
        # mydb.commit()
        database.source("add_evidence.sql", case_id, imgbb_url, output=False)
        # return "Image uploaded and link stored in database successfully"
        print(case_id)
        did = database.source("get_detective.sql", case_id)[0][0]
        return redirect(url_for('detectivepage', did=did))
    return render_template("evidence.html", var="Uploadimage")


@app.route('/Case', methods=['GET', 'POST'])
def case():
    if request.method == 'POST':
        case_id = request.form['case_id']
        p_o_c = request.form['p_o_c']
        det_id = request.form['det_id']
        case_details = request.form['case_details']
        database.callproce(case_id, p_o_c, det_id, case_details)
        return redirect(url_for('adminpage'))
    return render_template("new_form2.html", var="Case")

@app.route('/Cases', methods=['GET', 'POST'])
def cases():
    if request.method == 'POST':
        case_id = request.form['case_id']
        p_o_c = request.form['p_o_c']
        det_id = request.form['det_id']
        case_details = request.form['case_details']
        database.source("new_case.sql", case_id, p_o_c, det_id, 0, case_details, output=False)
        return redirect(url_for('adminpage'))
    return render_template("new_form2.html", var="Case")


@app.route('/Detective', methods=['GET', 'POST'])
def detective():
    if request.method == 'POST':
        det_id = request.form['det_id']
        det_name = request.form['det_name']
        gender = request.form['gender']
        age = request.form['age']
        adm_id = request.form['adm_id']
        database.source("new_detective.sql", det_id, det_name, gender, age, adm_id, output=False)
        return redirect(url_for('adminpage'))
    return render_template("new_form.html", var="Detective")

@app.route('/del/<case_id>')
def delete(case_id):
    did = database.source("get_detective.sql", case_id)[0][0]
    database.source("del_case.sql", case_id, output=False)
    return redirect(url_for('detectivepage', did=did))

@app.route('/view/<case_id>')
def view(case_id):
    # did = request.args["did"]
    try:
        database.source("selected_evidence.sql", case_id)
    except:
        evidence = []
    else:
        evidence = database.source("selected_evidence.sql", case_id)
    print(evidence)
    try:
        database.source("selected_victim.sql", case_id)
    except:
        victim = []
    else:
        victim = database.source("selected_victim.sql", case_id)
    print(victim)
    try:
        cri_id = database.source("find_cri.sql", case_id)[0][0]
        # print(cri_id)
        database.source("selected_criminal.sql", cri_id)
    except:
        criminal = []
    else:
        cri_id = database.source("find_cri.sql", case_id)[0][0]
        criminal = database.source("selected_criminal.sql", cri_id)
    print(criminal)
    try:
        case_details = database.source("get_case_details.sql", case_id)[0][0]
        # print(case_details)
    except:
        case_details = ""
    else:
        case_details = database.source("get_case_details.sql", case_id)[0][0]
    print(case_details)
    return render_template("viewcase.html",
                           case_id=case_id,
                           evidence=evidence, victim=victim,
                           criminal=criminal,
                           len_evi = len(evidence),
                           len_vic = len(victim),
                           len_cri = len(criminal),
                           case_details=case_details)



@app.route('/compare', methods=['GET', 'POST'])
def compare():
    if request.method == 'POST':
        file = request.files['image']
        image = Image.open(BytesIO(file.read()))
        img1 = np.array(image)

        # image_data_base64 = base64.b64encode(img1)

        all_fp_url = database.source("get_all_fingerprint.sql")
        print(all_fp_url)
        # print(img1)
        flag=0
        for each in all_fp_url:
            if compare_func(img1= img1,img2= each[0]) :
                # render data
                criminal = database.source("get_criminal_data.sql",each[0])[0]
                print(criminal)
                msg = "Fingerprint matched with criminal ID "+ criminal[0] + " and name: " + criminal[1]
                flash(msg)
                flag=1
                break
            img1 = np.array(image)
        if(flag!=1):
            msg="No match found"
            flash(msg)
        return redirect(url_for('compare'))
    return render_template("compare_form.html", var="compare")


@app.route('/clear')
def clear():
    database.clear()
    return redirect(url_for('index'))


@app.route('/Victim', methods=['GET', 'POST'])
def victim():
    if request.method == 'POST':
        case_id = request.form['case_id']
        vic_name = request.form['vic_name']
        vic_contact = request.form['vic_contact']
        database.source("add_victim.sql", case_id, vic_name, vic_contact, output=False)

        did = database.source("get_detective.sql", case_id)[0][0]
        return redirect(url_for('detectivepage', did=did))
    return render_template("victim_form.html", var="Victim")


@app.route('/edit/<case_id>')
def edit(case_id):
    database.source("edit_case.sql", case_id, output=False)
    did = database.source("get_detective.sql", case_id)[0][0]
    return redirect(url_for('detectivepage', did=did))


@app.route('/Fingerprint', methods=['GET', 'POST'])
def fingerprint():
    if request.method == 'POST':
        cri_id = request.form['cri_id']
        cri_name = request.form['cri_name']
        gender = request.form['gender']
        age = request.form['age']
        case_id = request.form['case_id']

        imgbb_api_key = "cb21bdae432dcb24b3a28484be9dcd60"
        imgbb_url = "https://api.imgbb.com/1/upload?key=" + imgbb_api_key
        image_file = request.files['image']
        image_data = image_file.read()
        image_name = image_file.filename
        # Encode the image data in base64
        image_data_base64 = base64.b64encode(image_data)

        # Set up the ImgBB API request
        imgbb_data = {
            "image": image_data_base64.decode(),
            "name": image_name
        }
        imgbb_response = requests.post(imgbb_url, data=imgbb_data)

        # Extract the image URL from the ImgBB API response
        imgbb_json = json.loads(imgbb_response.content)
        imgbb_url = imgbb_json["data"]["url"]
        # fp="b1.jpg"
        database.source("new_criminal.sql", cri_id, cri_name, imgbb_url, age, gender, output=False)
        database.source("involved_in.sql", case_id, cri_id, output=False)
        did = database.source("get_detective.sql", case_id)[0][0]
        return redirect(url_for('detectivepage', did=did))
    return render_template("addcriminal.html", var="Fingerprint")


@app.route('/login', methods=['POST', 'GET'])
def login():
    # Handles a user login
    if (request.method == 'POST'):
        user = User()
        success_flag = user.login()

        if (success_flag):
            if (user.da()):
                # flash('Your were logged in succesfully!', "success")
                return redirect(url_for('detectivepage', did = user.da()))
            else:
                # flash('Your were logged in succesfully!', "success")
                return redirect(url_for('adminpage'))
        else:
            flash('Error logging in', 'error')
            return redirect('/login')

    # Default GET route
    return render_template('login.html')



if __name__ == '__main__':
    app.secret_key = 'abc'
    app.run(debug= True)


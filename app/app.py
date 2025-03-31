from flask import Flask, render_template, request, url_for
from pymysql import connections
import os
import argparse


app = Flask(__name__)


# Connect to database
DBHOST = os.environ.get("DBHOST") or "127.0.0.1"
DBUSER = os.environ.get("DBUSER") or "root"
DBPWD = os.environ.get("DBPWD") or "pw"
DATABASE = os.environ.get("DATABASE") or "employees"
DBPORT = int(os.environ.get("DBPORT")) if os.environ.get("DBPORT") else 3306

# Create a connection to the MySQL database
db_conn = connections.Connection(
    host= DBHOST,
    port=DBPORT,
    user= DBUSER,
    password= DBPWD, 
    db= DATABASE
    
)
output = {}
table = 'employee'


# Resolve image path
from flask import send_from_directory

EXTERNAL_IMAGE_DIR = os.environ.get("IMAGE_DIR") or "bg_images"
IMAGE_FROM_ENV = os.environ.get("BG_IMAGE") or "bg1.jpg"
IMAGE = IMAGE_FROM_ENV

def resolve_image_path(image_name):
    return url_for('serve_external_image', filename=image_name)
    
@app.route("/external-images/<path:filename>")
def serve_external_image(filename):
    return send_from_directory(EXTERNAL_IMAGE_DIR, filename)


# APIs
@app.route("/", methods=['GET', 'POST'])
def home():
    image_path = resolve_image_path(IMAGE)
    return render_template('addemp.html', image=image_path)

@app.route("/about", methods=['GET','POST'])
def about():
    image_path = resolve_image_path(IMAGE)
    return render_template('about.html', image=image_path)
    
@app.route("/addemp", methods=['POST'])
def AddEmp():
    emp_id = request.form['emp_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    primary_skill = request.form['primary_skill']
    location = request.form['location']

  
    insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    try:
        
        cursor.execute(insert_sql,(emp_id, first_name, last_name, primary_skill, location))
        db_conn.commit()
        emp_name = "" + first_name + " " + last_name

    finally:
        cursor.close()

    print("all modification done...")
    image_path = resolve_image_path(IMAGE)
    return render_template('addempoutput.html', name=emp_name, image=image_path)

@app.route("/getemp", methods=['GET', 'POST'])
def GetEmp():
    image_path = resolve_image_path(IMAGE)
    return render_template("getemp.html", image=image_path)


@app.route("/fetchdata", methods=['GET','POST'])
def FetchData():
    emp_id = request.form['emp_id']

    output = {}
    select_sql = "SELECT emp_id, first_name, last_name, primary_skill, location from employee where emp_id=%s"
    cursor = db_conn.cursor()

    try:
        cursor.execute(select_sql,(emp_id))
        result = cursor.fetchone()
        
        # Add No Employee found form
        output["emp_id"] = result[0]
        output["first_name"] = result[1]
        output["last_name"] = result[2]
        output["primary_skills"] = result[3]
        output["location"] = result[4]
        
    except Exception as e:
        print(e)

    finally:
        cursor.close()

    image_path = resolve_image_path(IMAGE)
    return render_template("getempoutput.html", id=output["emp_id"], fname=output["first_name"],
                           lname=output["last_name"], interest=output["primary_skills"], 
                           location=output["location"], image=image_path)


if __name__ == '__main__':
    
    # Check for Command Line Parameters for color
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', required=False)
    args = parser.parse_args()

    if args.image:
        print("Image name from command line argument = " + args.image)
        IMAGE = args.image
    elif IMAGE_FROM_ENV:
        print("An image was set through environment variable - " + IMAGE_FROM_ENV)
        IMAGE = IMAGE_FROM_ENV
    else:
        print("No image was set.")


    app.run(host='0.0.0.0',port=8080,debug=True)

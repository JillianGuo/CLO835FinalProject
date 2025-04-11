from flask import Flask, render_template, request, url_for
from pymysql import connections
import os
from get_pic import download_pic


app = Flask(__name__)


# Connect to database
DBHOST = os.getenv("DBHOST", "localhost")
DBUSER = os.getenv("DBUSER", "root")
DBPWD = os.getenv("DBPWD", "pw")
DATABASE = os.getenv("DATABASE", "employees")
DBPORT = int(os.getenv("DBPORT", 3306))

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


BUCKET_NAME = os.getenv("BUCKET_NAME", "clo835-bgimages")
IMAGE = os.getenv("IMAGE", "bg1.jpg")
STATIC_DIR = os.getenv("STATIC_DIR", "static")
# Download the image from S3 bucket
download_pic(IMAGE, BUCKET_NAME, STATIC_DIR)


# APIs
@app.route("/", methods=['GET', 'POST'])
def home():
    image_path = url_for('static', filename=IMAGE)
    return render_template('addemp.html', image=image_path)

@app.route("/about", methods=['GET','POST'])
def about():
    image_path = url_for('static', filename=IMAGE)
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
    image_path = url_for('static', filename=IMAGE)
    return render_template('addempoutput.html', name=emp_name, image=image_path)

@app.route("/getemp", methods=['GET', 'POST'])
def GetEmp():
    image_path = url_for('static', filename=IMAGE)
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

    image_path = url_for('static', filename=IMAGE)
    return render_template("getempoutput.html", id=output["emp_id"], fname=output["first_name"],
                           lname=output["last_name"], interest=output["primary_skills"], 
                           location=output["location"], image=image_path)


if __name__ == '__main__':
    
    app.run(host='0.0.0.0',port=8080,debug=True)

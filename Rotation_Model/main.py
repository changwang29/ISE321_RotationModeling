# Import packages 
import math
import gurobipy as gp
from gurobipy import GRB
from flask import Flask, render_template, url_for, request, session 
from flask_sqlalchemy import SQLAlchemy  # This module is used for database management 
import os # set the path of the databse relative to the Flask app
from datetime import datetime 

# Database
basedir = os.path.abspath(os.path.dirname(__file__)) # Get the path of current file: base directory
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db') # Add databse file 
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True # Set database parameters using the apps configuration 
db = SQLAlchemy(app) # Bind the databse instance to our application 

# Define variables that relate to the column names in the table 
# 
class Store_Resident_data(db.Model):
  __tablename__ = 'resident'
  residentId = db.Column('Resident_id', db.Integer, primary_key = True) # Primary Key 
  # timestamp = db.Column('timestamp', db.DateTime)
  name = db.Column('name', db.String(50))
  # prolonged = db.Column('prolonged', db.String(50))
  allYear = db.Column('allYear', db.CHAR)
  # c3= db.Column('c3', db.Integer)
  # sex = db.Column('sex', db.CHAR)

  # Initialisation method to allow us to pass values for these fields
  def __init__(self, name,allYear):
    # self.timestamp = datetime.now()
    self.name = name
    self.allYear = allYear
    

class Store_Rotation_data(db.Model):
  __tablename__ = 'rotation'
  rotationId = db.Column('Rotation_id', db.Integer, primary_key = True) # Primary Key 
  # timestamp = db.Column('timestamp', db.DateTime)
  rotationName = db.Column('Rotation_name', db.String(50))
  # prolonged = db.Column('prolonged', db.String(50))
  mustDo = db.Column('MustDo', db.CHAR)
  busy = db.Column('busy', db.CHAR)
  # c3= db.Column('c3', db.Integer)
  # sex = db.Column('sex', db.CHAR)

  # Initialisation method to allow us to pass values for these fields
  def __init__(self, rotationName,mustDo,busy):
    # self.timestamp = datetime.now()
    self.rotationName = rotationName
    self.mustDo = mustDo
    self.busy = busy

@app.before_first_request
def create_tables():
    db.create_all()  

@app.route('/', methods=['GET', 'POST'])
def index():
  result = False
  if not os.path.exists(os.path.join(basedir, 'qtdata.db')):
    db.create_all()
  if request.method == 'POST':
    form = request.form

    # Store data to table
    residentName = request.form['residentName']
    allYear = request.form['allYear']
   
    
    # write the input data to the databse
    db.session.add(Store_Resident_data(residentName,allYear))
    db.session.commit()
    
    # render result 
    result = calculate(form)
  # render the index.html file stored in the templates folder
  return render_template('index.html', result=result)

@app.route('/index2', methods=['GET', 'POST'])
def index2():
  result = False
  if not os.path.exists(os.path.join(basedir, 'qtdata.db')):
    db.create_all()
  if request.method == 'POST':
    form = request.form

    # Store data to table
   
    rotationName = request.form['rotationName']
    mustDo = request.form['mustDo']
    busy = request.form['busy']
    
    # write the input data to the databse
    
    db.session.add(Store_Rotation_data(rotationName,mustDo, busy))
    db.session.commit()
    # render result 
    result = calculate(form)
  # render the index.html file stored in the templates folder
  return render_template('index2.html', result=result)


@app.route('/myData', methods=['GET'])
def myData():
  rotationDatas = Store_Rotation_data.query.all()
  return render_template('myData.html', rotationDatas=rotationDatas)

@app.route('/myData2', methods=['GET'])
def myData2():
  residentDatas = Store_Resident_data.query.all()
  return render_template('myData2.html', residentDatas=residentDatas)



def calculate(form):
  
  result = model()
  return result 
  
def model():
  return "a"
  

if __name__ == "__main__":
  app.run(debug=True)
  
import pyodbc 
from flask import Flask, request
from flask_restful import Resource, Api
from flask_jsonpify import jsonify
from flask_cors import CORS
import pdb
import base64
from utils import load_image,save_image
from reg.model import build_model, init_model
import sqlite3

import os, json



'''conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-SUH78IR\SQLEXPRESS;'
                      'Database=BitirmeProjesi;'
                      'Trusted_Connection=yes;')
                      '''

def get_initial(conection):
    with sqlite3.connect("BitirmeProjesi.db") as conn:
        cursor = conn.cursor()
        query = cursor.execute('SELECT id,FileId FROM students')
        data = []
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        return rows


app = Flask(__name__)

api = Api(app)
CORS(app)

BASE_DIR = 'reg'
IMAGES_BASE_DIR = os.path.join(BASE_DIR, 'database')
embedings_path = "Embedings.npz"

detection_params_path = os.path.join(BASE_DIR, 'detection_params.json')
recognization_params_path = os.path.join(BASE_DIR, 'recognization_params.json')

model = build_model(detection_params_path, recognization_params_path)
with sqlite3.connect("BitirmeProjesi.db") as conn:
    init_model(model, get_initial(conn), IMAGES_BASE_DIR,embedings_path)

class Studens(Resource):
    def get(self):
        with sqlite3.connect("BitirmeProjesi.db") as conn:
            cursor = conn.cursor() 
            q_string = 'SELECT * FROM students'
            
            query = cursor.execute(q_string)
            data = []
            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()
            data = {'data':[dict(zip(columns,row)) for row in rows]}
            


            return jsonify(data)

@app.route('/rollcall', methods=['POST'])
def SavePhoto():
    imagedata = request.get_data()
    imagestr = str(imagedata).split(",")[1]
    image = base64.decodestring(imagestr.encode('utf-8'))  
    bb, idxs = model(image)
    data = []
    for i in range(0,len(idxs)):
        data.append({"bb0":float(bb[i][0]),"bb1":float(bb[i][1]),"bb2":float(bb[i][2]),"bb3":float(bb[i][3]), "id": float(idxs[i])})
    return json.dumps(data)
@app.route('/AddNewStudent', methods=['POST'])
def AddNewStudent():
    newStudent = json.loads(request.get_data())

    Name = newStudent['Name']
    Namex =Name
    schoolNumber = newStudent['schoolNumber']
    images = newStudent['images']
    Namesplit = Namex.split(' ')
    
    filename=""
    for letter in Namesplit:
        filename+=letter[:2]
    filename+=str(schoolNumber)[-2:]
    idxsimage =0
    
    for image in images:
        imagefileName = filename
        imagefileName = imagefileName+str(idxsimage)
        image = base64.decodestring(image.encode('utf-8'))  
        path = os.path.join(IMAGES_BASE_DIR, filename)
        save_image(path,imagefileName,image)
        idxsimage = 1+idxsimage
    cursor = conn.cursor() 
    q_string = "INSERT INTO students ( Name, Schoolno, FileId) VALUES ('{0}','{1}', '{2}')".format(Name,schoolNumber,filename)
    query = cursor.execute(q_string)
    conn.commit()
    cursor.close()
    init_model(model, get_initial(conn), IMAGES_BASE_DIR,embedings_path)
    return jsonify(0)
        
        
        

api.add_resource(Studens, '/students') # Route_1



if __name__ == '__main__':
    app.run(port='5002')
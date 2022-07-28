from flask import Flask, render_template, request, jsonify, Response
import psycopg2
# from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
# import yaml
import requests
import csv

app = Flask(__name__, template_folder='templates')
# db_config = yaml.safe_load(open('database.yaml'))
# app.config['SQLALCHEMY_DATABASE_URI'] = db_config['uri']
# db = SQLAlchemy(app)
CORS(app)

conn = psycopg2.connect(
        host="ec2-44-206-117-24.compute-1.amazonaws.com",
        port="5432",
        database="d5knigjrb5pdph",
        user="euxqqreycxujvt",
        password="6fb679bd22aec45667687c79a3e4ed958c81cf584b489302a1bb38a9fe397469")

cur = conn.cursor()
# t_host = "ec2-44-206-117-24.compute-1.amazonaws.com"  # either "localhost", a domain name, or an IP address.
# t_port = "5432"  # default postgres port
# t_dbname = "d5knigjrb5pdph"
# t_user = ""
# t_pw = "6fb679bd22aec45667687c79a3e4ed958c81cf584b489302a1bb38a9fe397469"

# class User(db.Model):
#     __tablename__ = "users"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255))
#     age = db.Column(db.String(255))
#
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#
#     def __repr__(self):
#         return '%s/%s/%s' % (self.id, self.name, self.age)


t_host = "ec2-44-206-117-24.compute-1.amazonaws.com"  # either "localhost", a domain name, or an IP address.
t_port = "5432"  # default postgres port
t_dbname = "d5knigjrb5pdph"
t_user = "euxqqreycxujvt"
t_pw = "6fb679bd22aec45667687c79a3e4ed958c81cf584b489302a1bb38a9fe397469"

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/mandsDemoOrg/getLeads', methods=['GET'])
def data():

    if request.method == 'GET':
        url = "http://api.coincap.io/v2/assets"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        response = requests.request("GET", url, headers=headers, data={})
        myJson = response.json()
        ourData = []
        csvHeader = ["SYMBOL", "NAME", "PRICE(ISD)"]
        for x in myJson["data"]:
            listing = [x["symbol"], x["name"], x["priceUsd"]]
            ourData.append(listing)

        with open('crypto.csv', "w", encoding="UTF8", newline="") as f:
            writer = csv.writer(f)

            writer.writerow(csvHeader)
            writer.writerows(ourData)

        with open("crypto.csv") as fp:
            newCsv = fp.read()

        return Response(
            newCsv,
            mimetype="text/csv",
            headers={"Content-disposition":
                         "attachment; filename=leads.csv"})

if __name__ == '__main__':
    app.debug = True
    app.run()

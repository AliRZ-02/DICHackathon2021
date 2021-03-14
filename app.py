# Name: Get Lepton
# Date: Jan 8 2021
# Purpose: Flask App running the modeler in the backend

# Import Statements
import math
import sqlalchemy
from Predictor import interactions
from static import getData
from static import climateData
import csv
from flask import Flask, render_template, request, redirect, flash
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import difflib

# Creating the Flask App and Configuring the Database through SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///requests.db'
db = SQLAlchemy(app)

# Class that handles the database and the columns present in it
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(200), nullable=False)
    temp = db.Column(db.Integer, primary_key=False)
    graph = db.Column(db.String(200))
    lat = db.Column(db.Integer, primary_key=False)
    long = db.Column(db.Integer, primary_key=False)
    year = db.Column(db.Integer, primary_key=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

# Main Website URL - Uses index.html


@app.route('/', methods=['GET', 'POST'])
def index():
    db.drop_all()
    db.create_all()
    return render_template('homePage.html')


@app.route('/visualizations', methods=['GET', 'POST'])
def visualizations():
    print("VISUALIZATIONS PAGE")
    print(str(request.method))
    if str(request.method) == 'POST':
        print("POST")
        try:
            print("Searching")
            city_name = request.form['city_name']
            year = round(float(request.form['year']))
        except:
            print("Error")
            return redirect('/visualizations')
        readerAHCCD3 = csv.reader(open('static/Resources/AHCCD3.csv', 'r', encoding="ISO-8859-1"))
        cities = {}
        name_list = []

        for name, id in readerAHCCD3:
            cities[name.lower()] = id
            name_list.append(name.lower())

        # Uses the difflib library to find the closest name match to the input name
        try:
            matches = difflib.get_close_matches(city_name.lower(), name_list, n=1, cutoff=0.8)
            city = matches[0]
            print(city)
            good = cities[matches[0]]
            ahccd3 = True
        except:
            readerCLIMATE = csv.reader(open('static/Resources/CLIMATE.csv', 'r', encoding="ISO-8859-1"))
            cities2 = {}
            name_list2 = []
            ahccd3 = False

            for name, id in readerCLIMATE:
                cities2[name.lower()] = id
                name_list2.append(name.lower())
            try:
                matches = difflib.get_close_matches(city_name.lower(), name_list2, n=1)
                city = matches[0]
                good = cities2[matches[0]]
            except Exception as e:
                print("Error: ", e)
                return redirect('/visualizations')
        if ahccd3:
            print(year)
            getter = getData.get_data(name=city, number=good, neededYear=year)
            lat, long = getData.get_lat_long(number=good)
        else:
            getter = climateData.climate_data(name=city, number=good, year=year)
            lat, long = climateData.get_lat_long(number=good)
        if getter == -900:
            getter = "N/A"
        new_city = Todo(city=(city.upper()), temp=getter, graph=("../static/" + city.upper() + ".png"),
                        year=year, lat=lat, long=long)
        db.session.add(new_city)
        db.session.commit()
        print(getter)
        print(city)
        print("../static/" + city + ".png")
        return redirect('/visualizations')
    else:
        print('GET')
        cities = Todo.query.order_by(Todo.date_created.desc()).all()
        return render_template('visualizations.html', cities=cities)


if __name__ == "__main__":
    db.drop_all()
    db.create_all()
    app.run(debug=True)

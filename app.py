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
    temp = db.Column(db.Integer)
    graph = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

# Main Website URL - Uses index.html


@app.route('/', methods=['GET', 'POST'])
def index():
    print("Here")
    return redirect('/visualizations')

@app.route('/visualizations', methods=['POST', 'GET'])
def visualizations():
    if request.method == 'POST':
        print("Here")
        try:
            city_name = request.form['city_name']
            year = round(float(request.form['year']))
        except:
            print("Error")
            return redirect('/visualizations')
        print("Here")
        readerAHCCD3 = csv.reader(open('static/Resources/AHCCD3.csv', 'r', encoding="ISO-8859-1"))
        cities = {}
        name_list = []

        for name, id in readerAHCCD3:
            cities[name] = id
            name_list.append(name)

        # Uses the difflib library to find the closest name match to the input name
        try:
            matches = difflib.get_close_matches(city_name, name_list, n=1)
            city = matches[0]
            good = cities[matches[0]]
            ahccd3 = True
        except:
            readerCLIMATE = csv.reader(open('static/Resources/CLIMATE.csv', 'r', encoding="ISO-8859-1"))
            cities2 = {}
            name_list2 = []
            ahccd3 = False

            for name, id in readerCLIMATE:
                cities2[name] = id
                name_list2.append(name)
            try:
                matches = difflib.get_close_matches(city_name, name_list, n=1)
                city = matches[0]
                good = cities2[matches[0]]
            except:
                print("Man")
                return redirect('/visualizations')
        if ahccd3:
            getter = getData.get_data(name=city, number=good, year=year)
        else:
            getter = climateData.climate_data(name=city, number=good, year=year)
        new_city = Todo(city=city, temp=getter, graph=("../static/" + city + ".png"))
        db.session.add(new_city)
        db.session.commit()
        print(getter)
        print(city)
        print("../static/" + city + ".png")
        return redirect('/results')
    else:
        cities = Todo.query.order_by(Todo.date_created.desc()).all()
        return render_template('visualizations.html', cities=cities)


@app.route('/error', methods=['POST', 'GET'])
def error():
    return index()


if __name__ == "__main__":
    app.run(debug=False)

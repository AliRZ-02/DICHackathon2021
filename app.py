# Name: Get Lepton
# Date: Jan 8 2021
# Purpose: Flask App running the modeler in the backend

# Import Statements
import math
import sqlalchemy
from Predictor import interactions
from flask import Flask, render_template, request, redirect, flash
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# Creating the Flask App and Configuring the Database through SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///requests.db'
db = SQLAlchemy(app)

# Class that handles the database and the columns present in it
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    photo = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

# Main Website URL - Uses index.html


@app.route('/', methods=['GET'])
def index():
    return render_template('homePage.html')


@app.route('/visualizations', methods=['POST', 'GET'])
def visualizations():
    if request.method == 'POST':
        try:
            city_name = request.form['city_name']
            year = round(float(request.form['year']))
        except:
            return redirect('/visualizations')
        


@app.route('/error', methods=['POST', 'GET'])
def error():
    return index()


def reduce_db():
    # Reduce DB Elements by collecting all current db elements and removing older queries or User-Generated queries
    players = Todo.query.order_by(Todo.date_created).all()
    if len(players) > 5:
        for player in players:
            if player.name == "User-Generated-F" or \
                player.name == "User-Generated-D" or \
                player.name == "User-Generated-G":
                    db.session.delete(player)
                    db.session.commit()
            else:
                pass
        players = Todo.query.order_by(Todo.date_created).all()
        if len(players) > 5:
            db.session.delete(players[0])
            db.session.commit()
    else:
        pass


def check_duplicates(content):
    # removes db element if another copy already exists
    players = Todo.query.order_by(Todo.date_created).all()
    for player in players:
        if content.name == player.name:
            db.session.delete(player)
            break
        else:
            pass


if __name__ == "__main__":
    app.run(debug=False)

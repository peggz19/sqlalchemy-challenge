# Import the dependencies.
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

#1. Main Page
@app.route("/")
def main():
    """List all available api routes."""
    return (
        'Welcome to our API<br/>'
        f"Available Routes:<br/>"  
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f'/api/v1.0/date/yyyy-mm-dd<start><br/>'
        f'/api/v1.0/date/yyyy-mm-dd/yyyy-mm-dd<start>/<end><br/>'
    )

#2.Precipitation Page
@app.route("/api/v1.0/precipitation")
def prcp(): #first we query what we are looking for which are each dates and theyr respective prcp level
    last_12_months = session.query(measurement.date, measurement.prcp)\
                .filter((measurement.date < '2017-08-23')&(measurement.date >=(dt.date(2017,8,23)-dt.timedelta(days=365)))).\
                order_by(measurement.date).all()
    output = [] #then we pass it onto a dictionary
    for date,prcp in last_12_months:
        pass_dict = {}
        pass_dict['date']  = date
        pass_dict['prcp'] = prcp
        output.append(pass_dict)        
    return jsonify(output)

#3. Stations Page
@app.route("/api/v1.0/stations")
def stations(): 
    stations = session.query(measurement.station,func.count(measurement.station)).group_by(measurement.station)\
            .order_by(func.count(measurement.station).desc()).all()
    output = []
    counter = 0
    for i in stations:
        pass_dict = {}
        pass_dict['station'] = stations[counter][0]
        pass_dict['total'] = stations[counter][1]
        output.append(pass_dict)
        counter = counter + 1
    return jsonify(output)

#4. Tobs page
@app.route("/api/v1.0/tobs")
def tobs():
    last_12 = session.query(measurement.date,measurement.tobs).filter(measurement.station=='USC00519281').\
            filter((measurement.date < '2017-08-23')&(measurement.date >=(dt.date(2017,8,23)-dt.timedelta(days=365)))).all()
    output = []
    for date,tobs in last_12:
        pass_dict = {}
        pass_dict['date']  = date
        pass_dict['tobs'] = tobs
        output.append(pass_dict)        
    return jsonify(output)

#5.1 Start and End Date
@app.route("/api/v1.0/date/<start>")
def date(start):
    #First we put our query into a list 
    dict_ = []
    temps = session.query(measurement.date,measurement.tobs).all()
    for date,tobs in temps:
        pass_dict = {}
        pass_dict['date'] = date
        pass_dict['tobs'] = tobs
        dict_.append(pass_dict)

    #Second, we create a query that's going to give back min, max and avg values based on the above dict.
    #And we load the result into a list
    lsit = []
    for i in dict_:
       if i['date']==start:
            output = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs))\
                .filter(measurement.date>=i['date']).all()
            pass_dict = {}
            pass_dict['MIN'] = output[0][0]
            pass_dict['MAX'] = output[0][1]
            pass_dict['AVG'] = output[0][2]
            lsit.append(pass_dict)
            return jsonify(lsit)
            

#5.2 Start and End Given Dates
@app.route("/api/v1.0/date/<start>/<end>")
def datess(start,end):
    #First we put our query into a list 
    dict_ = []
    temps = session.query(measurement.date,measurement.tobs).all()
    for date,tobs in temps:
        pass_dict = {}
        pass_dict['date'] = date
        pass_dict['tobs'] = tobs
        dict_.append(pass_dict)

    #Second, we create a query that's going to give back min, max and avg values based on the above dict.
    #And we load the result into a list
    lsit = []
    for i,c in dict_:
       if i['date']==start & c['date']==end:
            output = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs))\
                .filter(measurement.date>i['date']).filter(measurement.date<c['date']).all()
            pass_dict = {}
            pass_dict['MIN'] = output[0][0]
            pass_dict['MAX'] = output[0][1]
            pass_dict['AVG'] = output[0][2]
            lsit.append(pass_dict)
            return jsonify(lsit)

                
if __name__ == '__main__':
    app.run(debug=True)

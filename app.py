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
        f'/api/v1.0/date/<start><br/>'
        f'/api/v1.0/<start>/<end><br/>'
    )

#2.Precipitation Page
@app.route("/api/v1.0/precipitation")
def prcp(): #first we query what we are looking for
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
    for record in stations:
        output.append(record.station)
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

#5. Start and End Date
@app.route("/api/v1.0/date/<start>")
def date(start):
    dict_ = []
    temps = session.query(measurement.date,measurement.tobs).all()
    for date,tobs in temps:
        pass_dict = {}
        pass_dict['date'] = date
        pass_dict['tobs'] = tobs
        dict_.append(pass_dict)

    for i in dict_:
       if i['date']==start:
            output = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs))\
                .filter(measurement.date>i).all()
            values = print(output)
            return (f'The minimum value, the maximum value and the average are respectively {values}')
        #return jsonify(dict_) This works when line 105 to 108 are removed and line 109 (this one) ran
if __name__ == '__main__':
    app.run(debug=True)

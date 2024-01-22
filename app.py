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
        f'/api/v1.0/<start><br/>'
        f'/api/v1.0/<start>/<end><br/>'
    )

#2.Precipitation Page
@app.route("/api/v1.0/precipitation")
def prcp():
    last_12_months = session.query(measurement.date, measurement.prcp)\
                .filter((measurement.date < '2017-08-23')&(measurement.date >=(dt.date(2017,8,23)-dt.timedelta(days=365)))).\
                order_by(measurement.date).all()
    output = []
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
def stations():
    last_12 = session.query(measurement.date,measurement.tobs).filter(measurement.station=='USC00519281').\
            filter((measurement.date < '2017-08-23')&(measurement.date >=(dt.date(2017,8,23)-dt.timedelta(days=365)))).all()
    output = []
    for date,tobs in last_12:
        pass_dict = {}
        pass_dict['date']  = date
        pass_dict['prcp'] = tobs
        output.append(pass_dict)        
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True)

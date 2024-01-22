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
        f"Available Routes:<br/>"  #CHANGE TO REFLE
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f'/api/v1.0/<start><br/>'
        f'/api/v1.0/<start>/<end><br/>'
    )

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


if __name__ == '__main__':
    app.run(debug=True)

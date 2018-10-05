#import dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from datetime import datetime
import datetime as dt

from flask import Flask, jsonify

#Database Setup

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement 
Station = Base.classes.station 

session = Session(engine)

# latest_date = session.query(func.max(Measurement.date)).all()

# year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)


app = Flask(__name__)

@app.route("/")
def home():
    print("Server received request for 'home' page")
    return (
        f"Welcome to my homepage!<br/><br/>"
        f"Here are the available routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/stations<br/>")

@app.route("/api/v1.0/precipitation")
def prcp():
    print("Server received request for 'precipitation' page")
    results = session.query(Measurement.date, Measurement.prcp).\
                filter(Measurement.date > '2016-08-23').\
                order_by(Measurement.date.asc()).all()

    all_prcp = []

    for prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = prcp.date
        prcp_dict["measurement"] = prcp.prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def station():
    print("Server received request for 'station' page")
    results = session.query(Measurement.station).group_by(Measurement.station).all()

    return jsonify(results)

@app.route("/api/v1.0/tobs")
def temp():
    print("Server received request for 'temperature' page")
    results = session.query(Measurement.date, Measurement.tobs).\
            filter(Measurement.date > '2016-08-23').\
            order_by(Measurement.date.asc()).all()
    
    all_tobs = []

    for tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = tobs.date
        tobs_dict["temperature"] = tobs.tobs
        all_tobs.append(tobs_dict)
    
    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def start(start):

    start_date = datetime.strptime(start, '%Y-%m-%d')
   
    tmin, tavg, tmax = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), \
                            func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()[0]

    result = [{"Minimum":tmin},{"Maximum":tmax},{"Average":tavg}]
    
    return jsonify(result)


@app.route("/api/v1.0/<start>/<end>")
def StartEnd(start,end):

    start_date = datetime.strptime(start, '%Y-%m-%d')
    end_date = datetime.strptime(end, '%Y-%m-%d')

    tmin, tavg, tmax = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), \
                            func.max(Measurement.tobs)).filter(Measurement.date >= start_date).\
                            filter(Measurement.date <= end_date.all()[0]

        
    result = [{"Minimum":tmin},{"Maximum":tmax},{"Average":tavg}]
    
    return jsonify(result)
        
if __name__ == "__main__":
    app.run(debug=True)


### My VS code stopped working after I changed somethings, I wasn't even able to run solved homework
### I am not sure if this code still works but I tried to complete this as best I can
###

import numpy as np
import pandas as pd

import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#Database Setup

engine = create_engine("sqlite:///hawaii.sqlite")

#Automaping database

Base = automap_base()
Base.prepare(engine, reflect=True)

#Saving tables

M = Base.classes.measurement
S = Base.classes.station


#initializng flask
app = Flask(__name__)

#flask routes

@app.route("/")
def welcome():
        """List of all returnable API routes."""
        return(
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
        )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    Prcp = session.query(M.date, M.tobs).\
        filter(M.date >= "2016-08-24", M.date <= "2017-08-23").\
        all()
    
    List = [Prcp]

    session.close()

    return jsonify(List)
      
@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)

    stations = {}


    results = session.query(S.station, S.name).all()
    for x,stations in results:
        S[x] = stations

    session.close()

     return jsonify(S) 





@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)

 
    LDP = session.query(M.date).order_by(M.date.desc()).first()
    FDP = (dt.datetime.strptime(LDP[0],'%Y-%m-%d') \
                    - dt.timedelta(days=365)).strftime('%Y-%m-%d')


    measurments =   session.query(M.date, M.tobs).\
                filter(M.date >= FDP).\
                order_by(M.date).all()

    
    tobslist = []

    for date, x in measurments:
        dictionary3 = {}
        dictionary3[date] = x
        tobslist.append(dictionary3)

    session.close()

    return jsonify(tobslist)


@app.route("/api/v1.0/<start>")
def Tstart(start):

    session = Session(engine)

    startlist = []

    results =   session.query(  M.date,\
                                func.min(M.tobs), \
                                func.max(M.tobs), \
                                func.avg(M.tobs)).\
                        filter(M.date >= "2016-08-24").\
                        group_by(M.date).all()

    for dates,Tmin,Tmax,Tavg in results:
        dictionary = {}
        dictionary["Date"] = dates
        dictionary["TMIN"] = Tmin
        dictionary["TMAX"] = Tmax
        dictionary["TAVG"] = Tavg
        
        startlist.append(dictionary)

    session.close()    

    return jsonify(startlist)

@app.route("/api/v1.0/<start>/<end>")
def temp_range_start_end(start,end):


    
    session = Session(engine)

    startendlist = []

    results =   session.query(  M.date,\
                                func.min(M.tobs), \
                                func.max(M.tobs), \
                                func.avg(M.tobs)).\
                        filter(and_(M.date >= "2016-08-24", M.date <= "2017-08-23")).\
                        group_by(M.date).all()

    for dates, Tmin, Tmax, Tavg in results:
        dictionary2 = {}
        dictionary2["Date"] = dates
        dictionary2["TMIN"] = Tmin
        dictionary2["TMAX"] = Tmax
        dictionary2["TAVG"] = Tavg
        
        startendlist.append(dictionary2)

    session.close()    

    return jsonify(startendlist)
       
if __name__ == "__main__":
    app.run(debug=True)
    

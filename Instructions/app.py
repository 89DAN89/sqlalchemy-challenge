import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
#Creating engine
engine = create_engine("sqlite:///hawaii.sqlite")
#Automaping information
Base = automap_base()
Base.prepare(engine, reflect=True)

#Saving tables

M = Base.classes.measurement
S = Base.classes.station


#initializng flask
app = Flask(__name__)

@app.route("/")
def Start():
        """List of all returnable API routes."""
        return(
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/tobs_startdate/<date><br/>"
        f"/api/v1.0/tobs_starttoend/<date_start>/<date_end>"
        )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    Prcp = session.query(M.date, M.tobs).\
        filter(M.date >= "2016-08-24", M.date <= "2017-08-23").\
        all()
    
    List = [Prcp]
    
    return jsonify()
    

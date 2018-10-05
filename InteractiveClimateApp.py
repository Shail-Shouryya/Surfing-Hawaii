##### dependencies needed to run flask api with all the modules we need #####
from flask import Flask, jsonify
import datetime as dt
from datetime import datetime
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Database Set up
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect = True)

#save tables as variables
#Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

##### Set up Flask
app = Flask(__name__)

#home route
@app.route("/")
def home():
    return (
    "Hawaii Weather Data API<br/>"
    "/api/v1.0/precipitation<br/>"
    "/api/v1.0/stations<br/>"
    "/api/v1.0/tobs<br/>"
    )

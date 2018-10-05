###dependencies
from flask import Flask, jsonify

import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

from datetime import datetime

# Database Set up
engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect = True)

#save tables as variables
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

##### Set up Flask
app = Flask(__name__)

#home route
@app.route("/")
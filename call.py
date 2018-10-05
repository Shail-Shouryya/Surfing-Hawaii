##### dependencies needed to run flask api with all the modules we need #####
from flask import Flask, jsonify
import datetime as dt
from datetime import datetime
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Database Set up
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect = True)

#save tables as variables
### not sure why getting ###
#KeyError: 'measurement'
#
#During handling of the above exception, another exception occurred:
#
#Traceback (most recent call last):
#  File "call.py", line 16, in <module>
#    Measurement = Base.classes.measurement
#  File "C:\Users\Shail\Anaconda3\lib\site-packages\sqlalchemy\util\_collections.py", line #212, in __getattr__
#    raise AttributeError(key)
#AttributeError: measurement
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

### fixed KeyError, was forgetting to refernce SQLite file from Resources directory ###

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

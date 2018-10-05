##### dependencies needed to run flask api with all the modules we need #####
from flask import Flask, jsonify
import datetime as dt
from datetime import datetime
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np

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
    "Hawaii Interactive Weather Data <br/>"
    "/api/v1.0/precipitation<br/>"
    "/api/v1.0/stations<br/>"
    "/api/v1.0/tobs<br/>"
    "/api/v1.0/YYYY-MM-DD<br/>"
    "/api/v1.0/YYYY-MM-DD/YYYY-MM-DD"
    )

    
@app.route("/api/v1.0/stations")
def stations ():
    #this method returns a json list of stations from the dataset
    results = session.query(Station.station).all()
    all_stations = list(np.ravel(results)) #import the numpy package

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def temperature_tobs ():
    #Return a json list of Temperature Observations (tobs) for the previous year
    tobs_past_year = []
    results = session.query(Measurement.tobs).filter(Measurement.date >= "08-23-2017").all() #hard-coded the date since still having trouble figuring out how to store date in a Python object
    tobs_past_year = list(np.ravel(results))

    return jsonify(tobs_past_year)

#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
@app.route("/api/v1.0/<start>")
def start_only (start):
    start_date = datetime.strptime(start, '%Y-%m-%d')
    minimum_temperature = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start_date).scalar()
    #print(minimum_temperature)
    average_temperature = session.query(func.round(func.avg(Measurement.tobs))).filter(Measurement.date >= start_date).scalar()
    # print(average_temperature)
    maximum_temperature = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start_date).scalar()
    # print(maximum_temperature)
    result = [{"Minimum temperature":minimum_temperature} , {"Maximum temperature":maximum_temperature} , {"Average temperature":average_temperature}]
    
    return jsonify(result)

@app.route("/api/v1.0/<start>/<end>")
def start_and_end (start, end):
     start_date = datetime.strptime(start, '%Y-%m-%d')
     end_date = datetime.strptime(end, '%Y-%m-%d')
     minimum_temperature = session.query(func.min(Measurement.tobs)).filter(Measurement.date.between(start_date, end_date)).scalar()
     #print(minimum_temperature)
     average_temperature = session.query(func.round(func.avg(Measurement.tobs))).filter(Measurement.date.between(start_date, end_date)).scalar()
     # print(average_temperature)
     maximum_temperature = session.query(func.max(Measurement.tobs)).filter(Measurement.date.between(start_date, end_date)).scalar()
     # print(maximum_temperature)
        
     result = [{"Minimum temperature":minimum_temperature} , {"Maximum temperature":maximum_temperature} , {"Average temperature":average_temperature}]
    
     return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
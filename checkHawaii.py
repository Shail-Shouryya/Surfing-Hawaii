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
### not sure why but keep getting:
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

### ---------> fixed KeyError, was forgetting to reference SQLite file from Resources directory ###

# Set up Flask
app = Flask(__name__)


@app.route("/")
def home():
    return (
    "Hawaii Interactive Weather Data <br/>"
    "/api/v1.0/precipitation <br/>"
    "/api/v1.0/stations <br/>"
    "/api/v1.0/tobs <br/>"
    "/api/v1.0/YYYY-MM-DD <br/>"
    "/api/v1.0/YYYY-MM-DD/YYYY-MM-DD <br/>"
    "/api/v1.0/info"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():   
    ### still getting same error from Jupyter Notebook here: AttributeError: 'str' object has no attribute 'year'  ###
    #most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    #final_date = most_recent_date[0]
    #past_year = final_date.replace(year = (final_date.year - 1))
    #past_year = past_year.strftime("%Y-%m-%d")

    #precipation_list = []
    
    #found a way to make list using numpy by hard-coding the final date
    works = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= "08-23-2017").all()
    precipation_list = list(np.ravel(works))
    
    return jsonify (precipation_list)

@app.route("/api/v1.0/stations")
def stations():
    #this method returns a json list of stations from the dataset
    results = session.query(Station.station).all()
    all_stations = list(np.ravel(results)) #import the numpy package

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def temperature_tobs():
    #Return a json list of Temperature Observations (tobs) for the previous year
    tobs_past_year = []
    results = session.query(Measurement.tobs).filter(Measurement.date >= "08-23-2017").all() #hard-coded the date since still having trouble figuring out how to store date in a Python object
    tobs_past_year = list(np.ravel(results))

    return jsonify(tobs_past_year)

#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
@app.route("/api/v1.0/<start>")
def start_only(start):
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
def start_and_end(start, end):
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

@app.route("/api/v1.0/info")
def info():
    infoPrint = "/api/v1.0/precipitation <br/ > \
    •Query for the dates and temperature observations from the last year. <br/ > \
    •Convert the query results to a Dictionary using date as the key and tobs as the value. <br/ > \
    •Return the JSON representation of your dictionary. <br/ > \
    <br/ > \
    /api/v1.0/stations <br/ > \
    •Return a JSON list of stations from the dataset. <br/ > \
    <br/ > \
    /api/v1.0/tobs <br/ > \
    •Return a JSON list of Temperature Observations (tobs) for the previous year. <br/ > \
    <br/ > \
    /api/v1.0/YYYY-MM-DD and /api/v1.0/YYYY-MM-DD/YYYY-MM-DD <br/ > \
    •Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range. <br/ > \
    •When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.<br/ > \
    •When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive. <br/ > \
    <br/ > \
    <br/ > \
    End of api info <br/ >"
    
    return (infoPrint)


if __name__ == '__main__':
    app.run(debug=True)
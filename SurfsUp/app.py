# Import the dependencies.
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Calculate the date one year from the last date in data set.
year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
year_ago

# Close Session
session.close()

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def homepage():
    """List all available api routes."""
    return (
         f"Honolulu, Hawaii Climate API:<br/>"
         f"Available Routes:<br/>"
         f"/api/v1.0/precipitation<br/>"
         f"/api/v1.0/stations<br/>"
         f"/api/v1.0/tobs<br/>"
         f"/api/v1.0/start (replace start with selected date in yyyy-mm-dd format)<br/>"
         f"/api/v1.0/start/end (replace start/end with selected date in yyyy-mm-dd format) <br/>"
     )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of dates with precipitation"""
    # Perform a query to retrieve the data and precipitation scores
    last_year = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= year_ago).\
        order_by(Measurement.date).all()

    session.close()

    # Convert precipitation list into a dictionary
    precipitation_list = []
    for date, prcp in last_year:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        precipitation_list.append(precipitation_dict)

    # Return a list of jsonified preceipitation for the last 12 months
    return jsonify(precipitation_list)

@app.route("/api/v1.0/stations")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Design a query to calculate the total number of stations in the dataset
    stations = session.query(Station.station).all()

    session.close()

    # Convert list of stations into normal list
    station_list = list(np.ravel(stations))

    # Return a list of jsonified stations
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all the total observations"""
    # Using the most active station id
    # Query the last 12 months of temperature observation data for this station and plot the results as a histogram
    most_active = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == "USC00519281").\
        filter(Measurement.date >= year_ago).all()

    session.close()

    # Convert temperature observation list into a dictionary
    tobs_list = []
    for date, tobs in most_active:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_list.append(tobs_dict)

    # Return a list of jsonified date and temperature observation data for the previous 12 months
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of min, max, and average of specified start date"""
    start_data = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    session.close()

# Convert min, max, and average of specified start date into a dictionary
    start_date_list = []
    for min, max, avg in start_data:
        start_date_dict = {}
        start_date_dict["min"] = min
        start_date_dict["max"] = max
        start_date_dict["avg"] = avg
        start_date_list.append(start_date_dict)

    # Return a list of jsonified min, max, and average of specified start date
    return jsonify(start_date_list)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of min, max, and average of specified start date and end date"""
    start_end_data = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    session.close()

# Convert min, max, and average of specified start date and end date list into a dictionary
    start_end_date_list = []
    for min, max, avg in start_end_data:
        start_end_date_dict = {}
        start_end_date_dict["min"] = min
        start_end_date_dict["max"] = max
        start_end_date_dict["avg"] = avg
        start_end_date_list.append(start_end_date_dict)

    # Return a list of jsonified min, max, and average of specified start date and end date
    return jsonify(start_end_date_list)

if __name__ == '__main__':
    app.run(debug=True)

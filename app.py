#Dependencies and Setup
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.pool import StaticPool

#Import Flask
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite", 
    connect_args={"check_same_thread": False}, poolclass=StaticPool, echo=True)

#Reflect an existing database into a new model
Base = automap_base()

#Reflect the tables
Base.prepare(engine, reflect=True)

#Save References to Each Table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create Session (Link) From Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

#Home Route
@app.route("/")
def welcome():
     #List all available api routes
        return """<html>
            <h1>Honolulu, HI API routes:</h1>

            <p>Precipitation:</p>
            <ul>
                 <li><a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a></li>
            </ul>

            <p>Station:</p>
            <ul>
                <li><a href="/api/v1.0/stations">/api/v1.0/stations</a></li>
            </ul>

            <p>Temperature Observations:</p>
            <ul>
                <li><a href="/api/v1.0/tobs">/api/v1.0/tobs</a></li>
            </ul>

            <p>Start Day Analysis:</p>
            <ul>
                <li><a href="/api/v1.0/2017-03-14">/api/v1.0/2017-03-14</a></li>
            </ul>

            <p>Start & End Day Analysis:</p>
            <ul>
                <li><a href="/api/v1.0/2017-03-14/2017-03-28">/api/v1.0/2017-03-14/2017-03-28</a></li>
            </ul>
            </html>
            """

#Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
        # Convert the query results to a dictionary using 'date' as the key and 'prcp' as the value.

        # Calculate the date 1 year ago from the last data point in the database
        a_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

        # Design a Query to Retrieve the Last 12 Months of Precipitation Data Selecting Only the `date` and `prcp` Values
        precipitation_data = session.query(Measurement.date, Measurement.prcp).\
                filter(Measurement.date >= a_year_ago).\
                order_by(Measurement.date).all()

        # Convert list of tuples into a dictionary
        prcp_data_list = dict(precipitation_data)

        # Return JSON representation of dictionary
        return jsonify(prcp_data_list)

#Station Route
@app.route("/api/v1.0/stations")
def stations():
        # Design a Query to retrieve the stations from the dataset 
        stations = session.query(Station.station, Station.name).all()

        # Convert List of Tuples Into Normal List
        station_list = list(stations)

        # Return JSON List of Stations from the dataset
        return jsonify(station_list)

#TOBs Route
@app.route("/api/v1.0/tobs")
def tobs():
        # Query the most active station with the highest count of temperature observations
        active_count = session.query(Measurement.station, func.count(Measurement.station)).\
            group_by(Measurement.station).\
            order_by(func.count(Measurement.station).desc()).all()

        # Query for the Dates and Temperature Observations from a Year from the Last Data Point
        a_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

        # Design a Query to retrieve the dates and temperature observations
        # of the most active station ("USC00519281") for the last year of data.
        most_active_tobs = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.date >= a_year_ago).filter(Measurement.station == active_count[0][0]).\
                order_by(Measurement.date).all()

        # Convert List of Tuples Into Normal List
        tobs_data_list = list(most_active_tobs)

        # Return JSON List of Temperature Observations (tobs) for the Previous Year
        return jsonify(tobs_data_list)

# Start Day Route
@app.route("/api/v1.0/<start>")
def start_(start):
        #Query Start Day
        start_date = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                group_by(Measurement.date).all()

        # Convert List of Tuples Into Normal List
        start_date_list = list(start_date)

        # Return JSON List of Min Temp, Avg Temp and Max Temp for a Given Start Range
        return jsonify(start_date_list)

#Start-End Day Route
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
        start_end_date = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                filter(Measurement.date <= end).\
                group_by(Measurement.date).all()

        # Convert List of Tuples Into Normal List
        start_end_list = list(start_end_date)

        # Return JSON List of Min Temp, Avg Temp and Max Temp for a Given Start-End Range
        return jsonify(start_end_list)

#Define main behavior
if __name__ == "__main__":
    app.run(debug=True)

# Surfs-Up
![surfs](Images/surfs-up.png)

## Climate Analysis and Exploration
Python and SQLAlchemy are used to do basic climate analysis and data exploration of the climate database. All of the following analysis are completed using SQLAlchemy ORM queries, Pandas, and Matplotlib:
* Use the provided [hawaii.sqlite](Resources/hawaii.sqlite) file to complete your climate analysis and data exploration.

* Choose a start date and end date for your trip. Make sure that your vacation range is approximately 3-15 days total.

* Use SQLAlchemy `create_engine` to connect to your sqlite database.

* Use SQLAlchemy `automap_base()` to reflect your tables into classes and save a reference to those classes called `Station` and `Measurement`.

### Precipitation Analysis
* Design a query to retrieve the last 12 months of precipitation data.

* Select only the `date` and `prcp` values.

* Load the query results into a Pandas DataFrame and set the index to the date column.

* Sort the DataFrame values by `date`.

* Plot the results using the DataFrame `plot` method.

  ![precipitation](Images/precipitation(12-months).png)

* Use Pandas to print the summary statistics for the precipitation data.

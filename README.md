# Climate by Location Data Processing
## Requirements
- Python 2.7.5
- Pandas 0.17.0
- NumPy 1.7.1

## Data Processing

### Terminology
The source data consists of 3 kinds of data

  * *historical observed*  (for the past)
  * *historical model*  (for the past)
  * *projected model*  (for the past)

We will use the term *regime* to distinguish between these 3.  This
terminology isn't standard -- it just helps to have a term to use to
refer to this characteristic of the data in the instructions below and
in the code.  We use the abbreviations "hist-obs", "hist-mod", and
"proj-mod" to refer to these.

### Input Data Format
The stats script expects the input to be for:
- a given county
- a given temporal resolution (annual, monthly, seasonal)
- a given regime (historical observed, historical modeled, projected modeled)
- a given element variable (tasmax, tasmin, etc)

With the data formatted as follows:
```
variable_name,year,value
```

For example:
```
...
var1,2000,64
var1,2001,65
...
var2,2000,62
var2,2001,66
...
```

Where `variable_name` can be a series of models. The core utility here is that for any repeated dates,
statistics will be computed across the collection of models as described below.

`data/derived/input/COUNTY/TEMPORAL-RESOLUTION/REGIME/ELEMENT.csv`.

### Computing statistics for modeled data
For each file in the input data directory, run the relevant stats script: [annual](stats-annual) or [monthly/seasonal](stats-ms).

The computations are described [below](# Statistics Computations).

Split out into separate files by county, time category, and element;
Create a new header column and copy the header into each row it belongs to.

### Output Data Paths for Public Use
The following is expected by the client-side graphing application.

1. Arrange the stats outputs as follows:

  `data/derived/final/COUNTY/TEMPORAL-RESOLUTION/REGIME/stats/ELEMENT.csv`.

2. Copy the annual `hist-obs` regime data into the `final` directory.  
   The above two steps created a bunch of stats files in the `final` directory corresponding
   to the `hist-mod` and `proj-mod` regimes.  The climate widget application also needs
   the raw `hist-obs` data files for annual data, so copy them into that directory.

   Note, however, that the Climate Widget does not use 'hist-obs' data for monthly or seasonal.

An example directory tree is as follows:
```
data/
    ...
    37021/
          annual/
              hist-mod/stats/
                  37021-annual-hist-mod-stats-cooling_degree_day_18.3.csv
                  37021-annual-hist-mod-stats-days_prcp_abv_25.3.csv
                  ...
              hist-obs/
                  37021-annual-hist-obs-cooling_degree_day_18.3.csv
                  37021-annual-hist-obs-days_prcp_abv_25.3.csv
                  ...
              proj-mod/stats/
                  data/37021/annual/hist-obs/37021-annual-hist-obs-days_prcp_abv_25.3.csv
                  data/37021/annual/hist-obs/37021-annual-hist-obs-days_prcp_abv_25.3.csv
                  ...
          monthly/
              ...
          seasonal/
              ...
    ...
```

---
**TODO: update the following to reflect the current methodlogy**

# Statistics Computations
The following is a narrative form of the processing and transformation the stats scripts perform on the data.

## Annual Data

### Raw Annual Data
The raw annual data for each meteorological element in the climate widget consists of 3 groups:

 * observed historical  

   The observed historical data consists of one element value for each county for each
   of the years 1949-2009 for temperature and precipitation, and for the years
   1950-2006 for all other variables.

 * model historical  

   The model historical data consists of one element value for each of several models
   for each of several (rcp*) scenarios for each county for each of the years 1950-2005
   for temperature and precipitation, and for the years 1950-2004 for all other
   variables.

 * model projection  

   The model projection data consists of one element value for each of several models
   for each of several (rcp*) scenarios for each county for each of the years 2006-2099.

In the case of variables which have a threshold value, such as "number of days with tmax
above 35", each separate threshold value is treated as a separate element.

### Statistics for Annual Data

 * observed historical  

   No statistics were computed for the observed historical annual data --- the climate widget
   graphs simply show the raw observed historical values for each year for the the chosen
   county and element.  The values are shown as blue and red bars in the graph.

 * model historical  

   For the model historicl data, the graph shows a solid black line
   and a grey band behind it.  For each year, the position of the
   solid black line gives the median value for all models for that
   year, and the bottom and top of the grey band show the 10th and
   90th percentile values for all models for that year

 * model projection

   For the model historicl data, the graph shows a solid blue line and blue
   band for the rcp45 scenario models, and a solid red line and red band
   for the rcp85 scenario models.  The solid line shows the median value
   of all models for the given year, county, and element, and the bottom
   and top of the band show the 10th and 90th percentile values.

## Monthly Data

### Raw Monthly Data

The raw monthly data consists of the same 3 groups as described above for
annual data, except that we have monthly data for temperature and precipitation
only, and there is one value for each month in the given time period, rather
than one value for each year.

### Statistics for Monthly Data

 * observed historical  

   The monthly data graph for a chosen element and county shows one solid black line
   and two dashed black lines for the observed historial data.  For each month, the
   position of the solid black line shows the median of all of the element values
   for that month for all years of data, and the dotted lines show the 10th and 90th
   percentile values.  To say this a different way, for a given county, element, and
   month, the raw data consists of one value for each of multiple years.  The black
   line shows the media of these values, and the the dotted lines show the 10th and 90th
   percentile values.

 * model historical  

   The model historical data is not used in the climate widget graphs; no statistics
   were computed with this data.

 * model projection

   The monthly data graph for a chosen element and county shows a solid line
   and a colored band for the model projection data, in blue for the rcp45 scenario,
   and in red for the rcp85 scenario.  For each scenario, the positions of
   the line and band were computed as follows.  For a given county, element,
   month, and scenario, the raw data contains a value for M models for each
   of Y years.  For each of the M models, we compute the median value
   across all the years of data (for the given month only); this results in one
   value for each model, and we then take the median of all these model values;
   the result is a single number that is the height of the solid line.

   Note that this is a two-step process.  We start with M*Y values.  In the first
   step, we take the median of that model's list of Y values corresponding to Y years.
   The result of this first step is that we now have one value for each model.
   In the second step we take the median of these values.  So the first step
   aggregates within each model across all the years, and the second step
   aggregates across the models.

   We then repeat the above procedure 4 more times, with different aggregation
   computations in the first step: 10th percentile, 90th percentile, min, and max.
   The second step is always the same: take the median across all models.

   The solid line for each scenario shows the result when the first step involves
   the median, and the bottom and top of the band shows the result when the
   first step is the 10th and 90th percentile.

   In summary, for each scenario:

     * solid line:  
       the median across all models of { for each model, the median value across all years }
     * bottom of band:  
       the median across all models of { for each model, the 10th percentile value across all years }
     * top of band:  
       the median across all models of { for each model, the 90th percentile value across all years }


## Seasonal Data

### Raw Seasonal Data

The raw seasonal data is exactly the same as the raw monthly data as described above,
except that data is only present for the months of Jan, Apr, Jul, and Oct, corresponding
to Winter, Spring, Summer, and Fall.

### Statistics for Seasonal Data

The statistics that were done for the seasonal data are exactly the same as for
the monthly data, except that each statistic was done for the 4 seasons rather
than for 12 months.

The seasonal graphs are shown using box plots rather than lines and
bands, but the data is the same: the solid central line in each box
represents the median across models of the median across years for
each model, and the bottom/top of the box represents the median across
models of the 10th/90th percentile across years for each model.

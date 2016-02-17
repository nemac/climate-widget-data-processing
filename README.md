# Climate Widget Time Series Graph Data Files and Processing

This document describes the time series data files used by the climate widget graphs,
and the processing used to generate them.

## Terminology

### Regime

The source data consists of 3 different time series:

  * *historical observed*  (for the past)
  * *historical model*  (for the past)
  * *projected model*  (for the future)

We will use the term *regime* to distinguish between these series.  This
terminology isn't standard -- it just helps to have a term to use to
refer to this grouping of the data in the documentation below and
in the code.  We use the abbreviations *hist-obs*, *hist-mod*, and
*proj-mod* to refer to these.

### Frequency

The source data also consist of time series using 3 different temporal
frequencies: annual, monthly, and seasonal.  These frequencies are
present in the above regimes as follows:

  * *hist-obs* contains
      * annual, monthly, and seasonal data for the years 1949-2009 (inclusive)
  * *hist-mod*  contains
      * annual data for the years 1950-2005 (no monthly or seasonal data for this regime)
  * *projected model* contains
      * annual data for the years 2006-2099 (inclusive)
      * monthly data for the years 2006-2100 (inclusive)
      * seasonal data for the years 2006-2100 (inclusive)
      
### FIPS Codes

The climate widget graph data is organized by US County. Each county is
identified by a unique 5-digit code called the [FIPS Code](https://en.wikipedia.org/wiki/FIPS_county_code).
Note that the FIPS code is always a 5-digit value, even when the first digit is 0.

### Units

All data files contain values given in metric units.  The climate widget graph
software converts these units to the English system at the time
that each graph is displayed.

### Parameters

The meteorological parameters present in the data are as follows:

  * for annual, monthly, and seasonal data:

    ```
    ID                           UNITS       DESCRIPTION 
    tasmax                       °C          mean daily maximum temperature 
    tasmin                       °C          mean daily minimum temperature 
    pr                           mm/day      mean daily average precipitation
    ```
    
  * for annual data only:
  
    ```
    ID                           UNITS       DESCRIPTION 
    cooling_degree_day_18.3      °C-day      cooling degree days relative to 18.3 °C
    heating_degree_day_18.3      °C-day      heating degree days relative to 18.3 °C
    days_tmax_abv_35.0           days        number of days with maximum temperature above 35.0 °C
    days_tmin_blw_0.0            days        number of days with minimum temperature below 0.0 °C
    days_prcp_abv_25.3           days        number of days with precipitation above 25.3 mm
    ```
    
### Raw Data vs Statistics Data

Some of the data used in the climate widget graphs comes directly from the original
source files; we call this "raw" data, meaning simply that the original values are
used directly.  Much of the data displayed in the graphs, however, involves computing
some statistic from the raw data, such as a mean, median, minimum, maximum, 10th
percentile value, or 90th percentile value.  These values are called "statistics"
(or "stats" for short) in this documentation.

Note that the distinction between "raw" and "stats" data simply refers
to whether or not a statistic was computed from the original data in
the process of creating the climate widget graph.  The original "raw"
data actually already consists of values which are computed
statistics of other values -- such as an average over a geographic
region, or an averge of daily values over a year, month, or season.

## Directory and Filename Structure

The raw data is contained in files using the following
directory and file name convention:

    FIPS/FREQUENCY/REGIME/FIPS-FREQUENCY-REGIME-PARAMETER_ID.csv

where

  * `FIPS` is a 5-digit county FIPS code
  * `FREQUENCY` is either "annual", "monthly", or "seasonal"
  * `REGIME` is either "hist-obs", "hist-mod", or "proj-mod"
  * `PARAMETER_ID` is the id of one of the meteorological parameters described above
  
The statistics data files use a similar convention but are stored
in a "stats" subdirectory of the regime directories, and include the
word "stats" in the filename:

    FIPS/FREQUENCY/REGIME/stats/FIPS-FREQUENCY-REGIME-stats-PARAMETER_ID.csv

For example, the raw annual proj-mod data for the tasmax parameter
for county 37021 is in the file `37021/annual/proj-mod/37021-annual-proj-mod-tasmax.csv`,
and the corresponding statistics values are in the file
`37021/annual/proj-mod/stats/37021-annual-proj-mod-stats-tasmax.csv`

## Statistics Computations

The following statistics are computed from the raw data, based on
the regime and frequency:

 * annual:
 
     * hist-obs: no stats are computed - the graphs show the raw hist-obs annual data directly

     * hist-mod: for each year of historical model data, compute the median, minimum,
       maximum, 10th-percentile, and 90th-percentile value across all model values for that
       year.
       
       This computation is done by the `stats-annual` script using the command:
       ```
       stats-annual  -g '' '.*' INPUT_FILE OUTPUT_FILE
       ```
       For example, the command to create the stats file corresponding to the
       raw data file `37021/annual/hist-mod/37021-annual-hist-mod-tasmax.csv` would be:
       ```
       stats-annual  -g '' '.*' \
           37021/annual/hist-mod/37021-annual-hist-mod-tasmax.csv \
           37021/annual/hist-mod/stats/37021-annual-hist-mod-stats-tasmax.csv
       ```
       
     * proj-mod: for each year of model projection data, and for each scenario, compute the median, minimum,
       maximum, 10th-percentile, and 90th-percentile value across all model values for that
       year and scenario.
        
       This computation is done by the `stats-annual` script using the command:
       ```
       stats-annual -g 'rcp45' '.*rcp45.*' -g 'rcp85' '.*rcp85.*'  IN OUT
       ```
       For example, the command to create the stats file corresponding to the
       raw data file `37021/annual/proj-mod/37021-annual-proj-mod-tasmax.csv` would be:
       ```
       stats-annual -g 'rcp45' '.*rcp45.*' -g 'rcp85' '.*rcp85.*' \
           37021/annual/proj-mod/37021-annual-proj-mod-tasmax.csv \
           37021/annual/proj-mod/stats/37021-annual-proj-mod-stats-tasmax.csv
       ```

 * monthly:
 
     * hist-obs: for each of the 12 calendar months, compute the median, minimum,
       maximum, 10th-percentile, and 90th-percentile values across all years
       present in the raw data.  Additionally, compute the mean value across
       the 30 years 1960-1989 (inclusive).  (This mean value, labelled as 'mean30'
       in the stats file, was used in an earlier version of the graphs and
       is no longer used but is still computed and included in the data.)
       
       This computation is done by the `stats-ms` script using the command
       ```
       stats-ms hist-obs INPUT_FILE OUTPUT_FILE
       ```
       For example, the command to create the stats file corresponding to
       the raw data file `37021/monthly/hist-obs/37021-monthly-hist-obs-tasmax.csv`
       would be:
       ```
       stats-ms hist-obs \
           37021/monthly/hist-obs/37021-monthly-hist-obs-tasmax.csv \
           37021/monthly/hist-obs/stats/37021-monthly-hist-obs-stats-tasmax.csv
       ```

     * hist-mod: monthly hist-mod data is not used, so no stats are computed for it
     
     * proj-mod: The following computation is done 3 times, once for each of the
       three 30-year time periods 2010-2039, 2035-2064, and 2060-2089.
       For each model in the raw data, and for each month
       in the calendar year, compute the mean value for that model and month
       over the 30 year period.  Then, for each month and each scenario, compute the median,
       minimum, maximum, 10th-percentile, and 90th-percentile values across
       all the models in that scenario.
     
       This computation is done by the `stats-ms` script using the command
       ```
       stats-ms proj-mod INPUT_FILE OUTPUT_FILE
       ```
       For example, the command to create the stats file corresponding to
       the raw data file `37021/monthly/proj-mod/37021-monthly-proj-mod-tasmax.csv`
 * seasonal:
 
   The stats computations for the seasonal data are exactly the same as for
   the monthly data, described above, because the structure of the seasonal
   data is the same as for the monthly data, except that each year only
   includes 4 values, corresponding to months 1,4,7, and 10.  The exact
   same commands described above for generating the monthly stats files
   from the monthly raw data will work for the seasonal raw data as well.


## Data File Formats

All data files, both raw and stats, are standard CSV files containing
newline-separated lines, each of which contains comma-separated values.
The first line of each file should be a heading line giving comma-separated
column names.  There should be no spaces or blank lines in any of the files.

The columns expected in each of the files are as follows:


 * annual
     * hist-obs raw
       would be:
       ```
       stats-ms proj-mod \
           37021/monthly/proj-mod/37021-monthly-proj-mod-tasmax.csv \
           37021/monthly/proj-mod/stats/37021-monthly-proj-mod-stats-tasmax.csv
       ```
     * hist-mod raw
       ```
       year
       <parameter_id>
       ```
       ```
       year
       <one column for each model; exact column names do not matter>
       ```
     * hist-mod stats
       ```
       year
       median
       min
       max
       p10
       p90
       ```
     * proj-mod raw
       ```
       year
       <one column for each model and scenario; name should include '_rcpNN_' string indicating which scenario>
       ```
     * proj-mod stats
       ```
       year
       rcp45median
       rcp45min
       rcp45max
       rcp45p10
       rcp45p90
       rcp85median
       rcp85min
       rcp85max
       rcp85p10
       rcp85p90
       ```
     
 * monthly
     * hist-obs raw
       ```
       yyyymm
       <parameter_id>
       ```
     * hist-obs stats
       ```
       month
       mean30
       max
       median
       min
       p10
       p90
       ```
     * proj-mod
       ```
       yyyymm
       <one column for each model and scenario; name should include '_rcpNN_' string indicating which scenario>
       ```
     * proj-mod stats 
       Note that in these column names, the first 4 digits give the center of one of
       the future 30-year periods of comparison.
       ```
       month
       2025rcp45_max
       2025rcp45_median
       2025rcp45_min
       2025rcp45_p10
       2025rcp45_p90
       2025rcp85_max
       2025rcp85_median
       2025rcp85_min
       2025rcp85_p10
       2025rcp85_p90
       2050rcp45_max
       2050rcp45_median
       2050rcp45_min
       2050rcp45_p10
       2050rcp45_p90
       2050rcp85_max
       2050rcp85_median
       2050rcp85_min
       2050rcp85_p10
       2050rcp85_p90
       2075rcp45_max
       2075rcp45_median
       2075rcp45_min
       2075rcp45_p10
       2075rcp45_p90
       2075rcp85_max
       2075rcp85_median
       2075rcp85_min
       2075rcp85_p10
       2075rcp85_p90
       ```
 * seasonal 
   The column names in the seasonal data files are exactly the same as in the monthly files.



## Example Data Files

The directory `37021` provided with this documentation contains a complete
set of all data files for one county.  Here is a list of all the files
in that directory:

```
37021/annual/hist-mod/37021-annual-hist-mod-cooling_degree_day_18.3.csv
37021/annual/hist-mod/37021-annual-hist-mod-days_prcp_abv_25.3.csv
37021/annual/hist-mod/37021-annual-hist-mod-days_tmax_abv_35.0.csv
37021/annual/hist-mod/37021-annual-hist-mod-days_tmin_blw_0.0.csv
37021/annual/hist-mod/37021-annual-hist-mod-heating_degree_day_18.3.csv
37021/annual/hist-mod/37021-annual-hist-mod-pr.csv
37021/annual/hist-mod/37021-annual-hist-mod-tasmax.csv
37021/annual/hist-mod/37021-annual-hist-mod-tasmin.csv
37021/annual/hist-mod/stats/37021-annual-hist-mod-stats-cooling_degree_day_18.3.csv
37021/annual/hist-mod/stats/37021-annual-hist-mod-stats-cooling_degree_day_18.3.csv.new
37021/annual/hist-mod/stats/37021-annual-hist-mod-stats-days_prcp_abv_25.3.csv
37021/annual/hist-mod/stats/37021-annual-hist-mod-stats-days_prcp_abv_25.3.csv.new
37021/annual/hist-mod/stats/37021-annual-hist-mod-stats-days_tmax_abv_35.0.csv
37021/annual/hist-mod/stats/37021-annual-hist-mod-stats-days_tmax_abv_35.0.csv.new
37021/annual/hist-mod/stats/37021-annual-hist-mod-stats-days_tmin_blw_0.0.csv
37021/annual/hist-mod/stats/37021-annual-hist-mod-stats-days_tmin_blw_0.0.csv.new
37021/annual/hist-mod/stats/37021-annual-hist-mod-stats-heating_degree_day_18.3.csv
37021/annual/hist-mod/stats/37021-annual-hist-mod-stats-heating_degree_day_18.3.csv.new
37021/annual/hist-mod/stats/37021-annual-hist-mod-stats-pr.csv
37021/annual/hist-mod/stats/37021-annual-hist-mod-stats-pr.csv.new
37021/annual/hist-mod/stats/37021-annual-hist-mod-stats-tasmax.csv
37021/annual/hist-mod/stats/37021-annual-hist-mod-stats-tasmax.csv.new
37021/annual/hist-mod/stats/37021-annual-hist-mod-stats-tasmin.csv
37021/annual/hist-mod/stats/37021-annual-hist-mod-stats-tasmin.csv.new
37021/annual/hist-obs/37021-annual-hist-obs-cooling_degree_day_18.3.csv
37021/annual/hist-obs/37021-annual-hist-obs-days_prcp_abv_25.3.csv
37021/annual/hist-obs/37021-annual-hist-obs-days_tmax_abv_35.0.csv
37021/annual/hist-obs/37021-annual-hist-obs-days_tmin_blw_0.0.csv
37021/annual/hist-obs/37021-annual-hist-obs-heating_degree_day_18.3.csv
37021/annual/hist-obs/37021-annual-hist-obs-pr.csv
37021/annual/hist-obs/37021-annual-hist-obs-tasmax.csv
37021/annual/hist-obs/37021-annual-hist-obs-tasmin.csv
37021/annual/proj-mod/37021-annual-proj-mod-cooling_degree_day_18.3.csv
37021/annual/proj-mod/37021-annual-proj-mod-days_prcp_abv_25.3.csv
37021/annual/proj-mod/37021-annual-proj-mod-days_tmax_abv_35.0.csv
37021/annual/proj-mod/37021-annual-proj-mod-days_tmin_blw_0.0.csv
37021/annual/proj-mod/37021-annual-proj-mod-heating_degree_day_18.3.csv
37021/annual/proj-mod/37021-annual-proj-mod-pr.csv
37021/annual/proj-mod/37021-annual-proj-mod-tasmax.csv
37021/annual/proj-mod/37021-annual-proj-mod-tasmin.csv
37021/annual/proj-mod/stats/37021-annual-proj-mod-stats-cooling_degree_day_18.3.csv
37021/annual/proj-mod/stats/37021-annual-proj-mod-stats-cooling_degree_day_18.3.csv.new
37021/annual/proj-mod/stats/37021-annual-proj-mod-stats-days_prcp_abv_25.3.csv
37021/annual/proj-mod/stats/37021-annual-proj-mod-stats-days_prcp_abv_25.3.csv.new
37021/annual/proj-mod/stats/37021-annual-proj-mod-stats-days_tmax_abv_35.0.csv
37021/annual/proj-mod/stats/37021-annual-proj-mod-stats-days_tmax_abv_35.0.csv.new
37021/annual/proj-mod/stats/37021-annual-proj-mod-stats-days_tmin_blw_0.0.csv
37021/annual/proj-mod/stats/37021-annual-proj-mod-stats-days_tmin_blw_0.0.csv.new
37021/annual/proj-mod/stats/37021-annual-proj-mod-stats-heating_degree_day_18.3.csv
37021/annual/proj-mod/stats/37021-annual-proj-mod-stats-heating_degree_day_18.3.csv.new
37021/annual/proj-mod/stats/37021-annual-proj-mod-stats-pr.csv
37021/annual/proj-mod/stats/37021-annual-proj-mod-stats-pr.csv.new
37021/annual/proj-mod/stats/37021-annual-proj-mod-stats-tasmax.csv
37021/annual/proj-mod/stats/37021-annual-proj-mod-stats-tasmax.csv.new
37021/annual/proj-mod/stats/37021-annual-proj-mod-stats-tasmin.csv
37021/annual/proj-mod/stats/37021-annual-proj-mod-stats-tasmin.csv.new
37021/monthly/hist-obs/37021-monthly-hist-obs-pr.csv
37021/monthly/hist-obs/37021-monthly-hist-obs-tasmax.csv
37021/monthly/hist-obs/37021-monthly-hist-obs-tasmin.csv
37021/monthly/hist-obs/stats/37021-monthly-hist-obs-stats-pr.csv
37021/monthly/hist-obs/stats/37021-monthly-hist-obs-stats-pr.csv.new
37021/monthly/hist-obs/stats/37021-monthly-hist-obs-stats-tasmax.csv
37021/monthly/hist-obs/stats/37021-monthly-hist-obs-stats-tasmax.csv.new
37021/monthly/hist-obs/stats/37021-monthly-hist-obs-stats-tasmin.csv
37021/monthly/hist-obs/stats/37021-monthly-hist-obs-stats-tasmin.csv.new
37021/monthly/proj-mod/37021-monthly-proj-mod-pr.csv
37021/monthly/proj-mod/37021-monthly-proj-mod-tasmax.csv
37021/monthly/proj-mod/37021-monthly-proj-mod-tasmin.csv
37021/monthly/proj-mod/stats/37021-monthly-proj-mod-stats-pr.csv
37021/monthly/proj-mod/stats/37021-monthly-proj-mod-stats-pr.csv.new
37021/monthly/proj-mod/stats/37021-monthly-proj-mod-stats-tasmax.csv
37021/monthly/proj-mod/stats/37021-monthly-proj-mod-stats-tasmax.csv.new
37021/monthly/proj-mod/stats/37021-monthly-proj-mod-stats-tasmin.csv
37021/monthly/proj-mod/stats/37021-monthly-proj-mod-stats-tasmin.csv.new
37021/seasonal/hist-obs/37021-seasonal-hist-obs-pr.csv
37021/seasonal/hist-obs/37021-seasonal-hist-obs-tasmax.csv
37021/seasonal/hist-obs/37021-seasonal-hist-obs-tasmin.csv
37021/seasonal/hist-obs/stats/37021-seasonal-hist-obs-stats-pr.csv
37021/seasonal/hist-obs/stats/37021-seasonal-hist-obs-stats-pr.csv.new
37021/seasonal/hist-obs/stats/37021-seasonal-hist-obs-stats-tasmax.csv
37021/seasonal/hist-obs/stats/37021-seasonal-hist-obs-stats-tasmax.csv.new
37021/seasonal/hist-obs/stats/37021-seasonal-hist-obs-stats-tasmin.csv
37021/seasonal/hist-obs/stats/37021-seasonal-hist-obs-stats-tasmin.csv.new
37021/seasonal/proj-mod/37021-seasonal-proj-mod-pr.csv
37021/seasonal/proj-mod/37021-seasonal-proj-mod-tasmax.csv
37021/seasonal/proj-mod/37021-seasonal-proj-mod-tasmin.csv
37021/seasonal/proj-mod/stats/37021-seasonal-proj-mod-stats-pr.csv
37021/seasonal/proj-mod/stats/37021-seasonal-proj-mod-stats-pr.csv.new
37021/seasonal/proj-mod/stats/37021-seasonal-proj-mod-stats-tasmax.csv
37021/seasonal/proj-mod/stats/37021-seasonal-proj-mod-stats-tasmax.csv.new
37021/seasonal/proj-mod/stats/37021-seasonal-proj-mod-stats-tasmin.csv
37021/seasonal/proj-mod/stats/37021-seasonal-proj-mod-stats-tasmin.csv.new
```

Terminology
===========

The source data consists of 3 kinds of data

  * *historical observed*  (for the past)
  * *historical model*  (for the past)
  * *projected model*  (for the past)

We will use the term *regime* to distinguish between these 3.  This
terminology isn't standard -- it just helps to have a term to use to
refer to this characteristic of the data in the instructions below and
in the code.  We use the abbreviations "hist-obs", "hist-mod", and
"proj-mod" to refer to these.


Steps
=====
For any temporal resolution (annual, seasonal, monthly), perform the following steps

1. Reformat the data.  
   Split out into separate files by county, time category, and element;
   Create a new header column and copy the header into each row it belongs to.

   Arrange the outputs as follows:
   `data/derived/reformatted/COUNTY/TEMPORAL-RESOLTUION/REGIME/ELEMENT.csv`.

2. Compute the statistics.  
   For each file in the reformatted directory, run the relevant stats script;
   - [annual](stats-annual)
   - [monthly or seasonal](stats-ms)

   Arrange the outputs as follows:
   `data/derived/final/COUNTY/TEMPORAL-RESOLTUION/REGIME/stats/ELEMENT.csv`.

3. Copy the annual `hist-obs` regime data into the `final` directory.  
   The above two steps created a bunch of stats files in the `final` directory corresponding
   to the `hist-mod` and `proj-mod` regimes.  The climate widget application also needs
   the raw `hist-obs` data files for annual data, so copy them into that directory.

   Note, however, that the Climate Widget does not use 'hist-obs' data for monthly or seasonal.

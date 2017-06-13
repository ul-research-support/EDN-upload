# EDN-upload

Instructions for uploading EDN data to Refugee Health

  1. Get EDN files from a Refugee Health Program Coordinator, typically sent within a .zip file.  Specifically you need:
  a. DS-2054.txt
  b. DS-3025-Vaccinations.txt
  c. Pre-departure.txt

  2. Put these in upload folder with the date of the upload (e.g. 08012016). 
     Also, add country_codes_clean.csv into the same folder.  

  3. Execute Process_Data.py (this is the library with many of the functions)

  4. Execute driver_rev1.py -- this will run, produce the departure_vaccinations.csv file and upload the data.

  5. Send the departure_vaccinations.csv to Beth Barnes for her to manually enter those vaccinations that script could not discriminate.

# Running the Scripts

Process Data must run first and should have no issues executing. Afterwards, it's time to run the driver script. Sometimes errors can crop up here, but these are rare.

For example, sometimes a ValueError pops up denoting a length mismatch. It can be fixed by adjusting the number of columns declared on the stated line (where the error was thrown) based on how many columns the expected axis is said to contain.

Pay attention to the comments in the code, as they will show you where to insert your filepath as well as corrrect file names. You'll find the filepath in the beginning of the driver file.

Ensure that all of your EDN files are named to match what is in the code (lines 21-24 of driver).

# Uploading the Data

You have two options for uploading: a straight upload using the REDCap API or a manual import of a CSV file.

If uploading through the API, make sure to comment out the CSV creation code (line 341) and to remove the quotation marks that encase the REDCap API script as a string at the end of the file. Remember, you need a REDCap API token to perform the upload this way. Also, if there are any errors in the dataset that is to be uploaded, the API upload will fail. It is recommended to go with a manual REDCap import until the process is further automated to eliminate errors.

If you are uploading via manual import, click Data Import Tool from the sidebar in REDCap and follow the instructions in REDCap to continue.

This is the preferred method due to recurring errors in the EDN datasets.

# Troubleshooting

When performing a manual import of EDN data via REDCap, it is not unusual to encounter errors with the data. These errors are usually a quick fix, and should be handled within the CSV file before attempting to re-upload.

Note: Oftentimes most errors encountered in the REDCap import method are due to country code discrepancies. Typically this occurs with Ukraine and South Africa specifically. This is because EDN and RedCAP fluctuate between two different country code standards: ISO (alpha-2) and FIPS 10-4.

In the MySQL database that REDCap connects to, the codes for these countries are assigned as follows:

    Ukraine: UA
    South Africa: SF
    
However, in the EDN files we receive, these countries will typically show up with different codes that can result in an import error:

    Ukraine: UP
    South Africa: ZA
    
This is a recurring issue with the data that we receive from EDN. In order to successfully import the full dataset, these country codes need to be changed manually within the CSV file to UA and SF. Until a workaround is made either in MySQL or REDCap, this will continue to be a part of the upload process.

For reference: http://www.nationsonline.org/oneworld/countrycodes.htm

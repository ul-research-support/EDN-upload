# EDN-upload
    Process_Data.py and driver.py authored by Dr. Robert Kelley, assistant professor 
    of computer science at St. Mary's College of Maryland. 

Instructions for uploading EDN data to Refugee Health:

  1. Get EDN files from a Refugee Health Program Coordinator, typically sent within a .zip file.  Specifically you need:
       a. DS-2054.txt
       b. DS-3025-Vaccinations.txt
       c. Pre-departure.txt

  2. Put these in upload folder with the date of the upload (e.g. 08012016). 
     Also, add country_codes_clean.csv into the same folder.  

  3. Execute Process_Data.py (this is the library with many of the functions)

  4. Execute driver.py -- this will run, produce the departure_vaccinations.csv file, and create a CSV upload file for REDCap import.

  5. Upload the CSV file using REDCap Data Import Tool. Be sure to review the final dataset for errors.

  6. Send the departure_vaccinations.csv to Beth Barnes for her to manually enter those vaccinations that script could not discriminate.

# Running the Scripts

Process Data must run first and should have no issues executing. Afterwards, it's time to run the driver script. Errors can crop up here if the EDN input fields change. If new fields are added, the script will need to be adjusted to accommodate them. One such change has already been written (and commented out on lines 186-195 of driver.py) to account for the new ovs_syphilis field.

Pay attention to the comments in the code, as they will show you where to insert your filepath as well as corrrect file names. You'll find the filepath in the beginning of the driver file. Ensure that all of your EDN files are named to match what is in the code (lines 21-24 of driver.py).

# Uploading the Data

You have two options for uploading: a straight upload using the REDCap API or a manual import of a CSV file.

If you wish to use the API, you need a REDCap API token to perform the upload this way. If there are any errors in the final dataset, the API upload will fail. It is recommended to go with a manual REDCap import until the process is further automated to eliminate all possible errors.

If you are uploading via manual import, click Data Import Tool from the sidebar in REDCap and follow the instructions in REDCap to  continue.

# Troubleshooting

When performing a manual import of EDN data via REDCap, it is not unusual to encounter some errors in the dataset. These errors are usually minor and quick to fix, they should be handled within the CSV file before attempting to re-upload. 

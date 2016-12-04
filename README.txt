NOTABLE REMARKS

1. 
- theatreDB.txt has been modified so that the foreign keys cascade on delete and update
- this file should be used instead of the default database file to reflect this change

2. 
- the code for the poster has been commented out
- currently the code inserts the image into the database as a BLOB
- however, the only issue is displaying the image in the table given encoding issues

3. flaskext module can be installed by running pip install flask-mysqldb
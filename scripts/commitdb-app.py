#!/usr/bin/python3
import appsitefunctions
import time
import cgi
import os.path
import mysql.connector

# Turn on debug mode.
import cgitb
cgitb.enable()

# This section will grab the name of the app server host name from the mtwa.conf file
servernames = appsitefunctions.importconfiguration() 
dbServerHostname = servernames[1]

# Connect to the database.
try:
    conn = mysql.connector.connect(
        host=dbServerHostname,
        user="appdemo",
        password="appdemo",
        database="appdemo"
    )
    c = conn.cursor()
    
    # Process the data from the HTML form
    form = cgi.FieldStorage()
    arg1 = form.getvalue('name')
    arg1 = arg1.replace("'", "\\'")  # Keeps single quotes from crashing the app because of the SQL statement
    arg2 = form.getvalue('notes')
    arg2 = arg2.replace("'", "\\'")  # Keeps single quotes from crashing the app because of the SQL statement
    arg3 = form.getvalue('count')
    arg3int = int(arg3) 
    numofrecords = arg3int
    
    # While loop to start entering the records into the MySQL server
    while arg3int > 0:
        currentdatetime = time.strftime("%Y-%m-%d %H:%M:%S")
        
        # Using parameterized query to avoid SQL injection
        sqlstring = "INSERT INTO demodata (name, notes, timestamp) VALUES (%s, %s, %s)"
        
        # Saves data to MySQL database with safe parameter handling
        c.execute(sqlstring, (arg1, arg2, currentdatetime))  # Execute the insert
        conn.commit()  # Commit the changes
        
        # Check if the last insert was successful
        result = 1 if c.rowcount > 0 else 0  # Set result to 1 if more than 0 rows were affected

        arg3int -= 1

    # Start HTML print out, headers are printed so the Apache server on APP does not produce a malformed header 500 server error
    print('''
    Content-type: text/html\n\n
    <html>
    <head>
    <title>Multi-Tier Web App</title>
    </head>
    <body>
    <table border="1">
    ''')

    # Checks to see if anything other than 1 is returned from c.execute()
    if result == 1:
        if numofrecords == 1:
            print('<br><center><h3>Saved %s Record to Database!</h3></center>' % numofrecords)
        else:
            print('<br><center><h3>Saved %s Records to Database!</h3></center>' % numofrecords)
    else:
        print('<h3>There was an error committing the information to the database</h3>')

    print('</center>')

    # Finish printing headers 
    print('''
    </table>
    </body>
    </html>
    ''')

except:
    appsitefunctions.printdbservererror()
finally:
    # Ensure the connection is closed
    if conn.is_connected():
        c.close()
        conn.close()
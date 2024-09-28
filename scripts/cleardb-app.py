#!/usr/bin/python3
from datetime import datetime
import cgi
import appsitefunctions

# Turn on debug mode.
import cgitb
cgitb.enable()

# This section will grab the name of the app server host name from the mtwa.conf file
servernames = appsitefunctions.importconfiguration() 
dbServerHostname = servernames[1]

# Connect to the database.
import mysql.connector
try:
    conn = mysql.connector.connect(
        host=dbServerHostname,
        user="appdemo",
        password="appdemo",
        database="appdemo"
    )
    c = conn.cursor() 

    # Process the data from the HTML form and check to see if data was entered.
    usercommand = 'nothing_entered'
    form = cgi.FieldStorage()

    if form.getvalue('command') is None:
        arg1 = 'null'
    else:
        arg1 = form.getvalue('command')
        usercommand = str.upper(arg1)

    # Used for the erase log
    currentdatetime = str(datetime.now())
    forsql_datetime = "\'" + currentdatetime + "\'"

    # Start HTML print out, headers are printed so the Apache server on APP does not produce a malformed header 500 server error
    print ('''
    <Content-type: text/html\\n\\n>
    <html>
    <head>
    <title>Multi-Tier Web App</title>
    </head>
    <body>
    <table border="1">
    ''')

    # Check the value of the string entered in the form and looks to see if the user entered the word "ERASE"
    if usercommand == 'ERASE':
        # First check if the table is empty
        c.execute("SELECT COUNT(*) FROM demodata;")
        row_count = c.fetchone()[0]

        if row_count == 0:
            # If the table is empty, set deleteresult to 0
            deleteresult = 0
            print('<br><center><h3>The table is already empty. No rows to delete.</center></h3>')
        else:
            # If the table is not empty, proceed to delete and set deleteresult to the number of affected rows
            deletetable = "TRUNCATE TABLE demodata;"  # Clear TABLE demodata even the primary key "ID" will be initialized
            logdelete = "INSERT INTO demodata_erase_log (timestamp) VALUES (" + forsql_datetime + ");"

            # Runs SQL command on MySQL database
            deleteresult = c.execute(deletetable)
            c.execute(logdelete)

            if deleteresult == 0:
                print('<br><center><h3>Data Erased From Database! No rows affected.</center></h3>')
            else:
                print(f'<br><center><h3>Data Erased From Database! {row_count} rows deleted.</center></h3>')

        conn.commit()
    else:
        print('<br><center><font color="red">Data NOT Cleared.  No command or incorrect command was entered.</font></center>')

    print('</center>')

    # Finish printing headers 
    print('''
    </table>
    </body>
    </html>
    ''')

except Exception as e:
    print(f"ERROR: {e}")
    appsitefunctions.printdbservererror()
finally:
    # Close the connection
    if conn.is_connected():
        conn.close()
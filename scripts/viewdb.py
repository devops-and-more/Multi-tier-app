#!/usr/bin/python3


#This is a "module" script, by which I mean that appsitefunctions.loadbasehtml() uses this to create a section of the site.

# Turn on debug mode.
import cgitb
cgitb.enable()
import appsitefunctions

#This section will grab the name of the app server host name from the mtwa.conf file
servernames=appsitefunctions.importconfiguration()
dbServerHostname=servernames[1]

# Connect to the database.
import mysql.connector
try:
    conn = mysql.connector.connect(
    host=dbServerHostname,
    user="appdemo",
    password="appdemo",
    database="appdemo")
    
    c = conn.cursor()
    
    #Grab the table data from the database.
    c.execute("SELECT * FROM demodata;") #SELECT * FROM demodata")
    
    #Start HTML print out, headers are printed so the Apache server on APP does not produce a malformed header 500 server error
    print ('''
    <Content-type: text/html\\n\\n>
    <html>
    <head>
    <title>Multi-Tier Web App</title>
    </head>
    <body>
    <table border="5">
    ''')
    
    #Start printing the html for the header row
    print ('<center><h3>View Data</h3></center>')
    result= c.fetchall()
        
    if not result :
        print('<p>Your database table is empty!!</p>')
    else:
        print('<table style="width:100%" border="1"><tr><td><b>ID</b></td><td><b>Name</b></td><td><b>Notes</b></td> <td><b>Timestamp</b></td> </tr>')
        for each in result:
            print ('<tr>')
            print ('<td>',each[0], '</td>')
            print ('<td>',each[1], '</td>')
            print ('<td>',each[2], '</td>')
            print ('<td>',each[3], '</td>')
            print ('</tr>')
        print('</table>')
        #Finish printing headers
    print ('''
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

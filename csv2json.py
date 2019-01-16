#!/usr/bin/env python

"""Creates a JSON file used for Zero Touch Provisioning (ZTP)

This script runs on a the service provisioning web server.
It retrieves a list of devices and associated attributes from
a CSV file and creates a JSON file. The Node.js service uses 
the file to return device attributes based on the device serial
number.

This script requires a filename called 'serial-ip.csv', to be
located in the same directory as the script. 

The 'serial-ip.csv' file must have column names as follows:
serial,ip,netmask,gw,config_url,hostname

Each row represents a single device with the following attributes:

    - Serial Number
    - IP address
    - Netmask
    - Default Gateway
    - Configuration URL (normally not required - leave blank)
    - Hostname
    
This script is located on the file system of the web server used
for ZTP.
"""

import csv
import json

# Open the CSV file

f = open( './serial-ip.csv', 'rU' )

# Load CSV field names

reader = csv.DictReader( f, fieldnames = ( "serial","ip","netmask","gw","config_url","hostname" ))

# Parse the CSV into JSON

out = json.dumps( [ row for row in reader ] )
jsondata = "{ \"device\": " + str(out) + " }"
print "JSON parsed!"

# Write out JSON data

f = open( './parsed.json', 'w')
f.write(jsondata)
f.close()
print "JSON saved!"

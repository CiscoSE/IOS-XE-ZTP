# IOS-XE-ZTP

Code for ZTP with IOS XE 16.9


## Business/Technical Challenge

Business Problem - Legacy devices in the customer network are approaching end of life milestones and need to be replaced. However, the customer does not always have enough staff resources to deploy the required quantity of new Cisco networking equipment. Additionally, new customer deployments are prone to error due to manual provisioning.

Technical Challenge - Develop a solution which enables the customer to auto-provision devices thus reducing deployment errors and saving staff resource time.

## Proposed Solution

Proposed Solution - Create a Python script with supporting services to auto-provision devices for Day 0 deployment.


### Cisco Products Technologies/ Services

The solution includes the following technologies:

Cisco Technology:
- Catalyst 9000 and 3650 series switches
- Cisco ENCS 5400 Branch NFV Platform
- Cisco ISRv virtual router
- IOS XE 16.9 with IOx guestshell support
- IBNS 2.0

Open Source:
- Ubuntu Linux server (open source)
- Apache2 WebServer (open source)
- ISC DHCP Server (open source)
- Node.js json-server (open source)
- Python 2.7 (open source)

## Team Members


* Bob Clay <boclay@cisco.com> - Global Enterprise
* Ameron Sheikh <imsheikh@cisco.com> - Commercial
* Jason Whiteaker <jawhitea@cisco.com> - Customer Experience


## Solution Components


<!-- This does not need to be completed during the initial submission phase  

Provide a brief overview of the components involved with this project. e.g Python /  -->

Solution components include:

* Files
* Open Source Tools
* Devices to be Provisioned

### Files

The files posted for this project include two Python scripts, a CSV file, and an IOS template.

The ZTP.py script contains the main Python program that runs in Guest Shell on the device. This script is automatically downloaded from a web server as identified in the DHCP reply when the network device boots onto the network for the first time.

The csv2json.py script is a server-side script which retrieves a list of devices and associated attributes from a CSV file and creates a JSON file. The Node.js service uses the JSON file to return device attributes based on the device serial number.

The serial-ip.csv file is a comma separated variable (CSV) file which contains a list of devices based on serial number. Each serial number corresponds to a list of device attributes such as hostname, IP address, etc. related to the devices' location in the network. 

The IBNS2.cfg file is an IOS template that contains commands for configuring an IOS XE 16 switch for use with ISE in a high security enviornment. The IOS configuraiton includes commands for AAA, Device Profiling, and an Interface Template for dot1x for the access ports. 

### Open Source Tools

The Open Source tools used for this project include the ISC DHCP server, Node.js, and Apache2 web server. These services are hosted on an Ubuntu virtual machine running on an ENCS-5400 appliance. 

The ISC DHCP server provides network parameters for the Catalyst switches upon boot-up. The DHCP scope includes Option 67 which specifies the URL for the ZTP.py script.

The Node.js server reads the JSON file which was created from the serial-ip.csv file. The JSON file contains the device attributes, and it returns those attributes as a REST reply back to the ZTP.py script running on the network device.

The Apache2 web server hosts the ZTP.py file and the IBNS2.cfg template.

### Devices to be Provisioned

Catalyst 9300 and 3650 switches are examples of devices which can be provisioned with this project. These devices run IOS XE 16.9 and therefore include the Guest Shell feature with onbox Python support. 

## Usage

<!-- This does not need to be completed during the initial submission phase  

Provide a brief overview of how to use the solution  -->

Plug the switch management port into the network and turn on the power. The switch will download ZTP.py and begin executing the script. In about 5 minutes, the switch will be on the network and fully provisioned.

Note - The solution requires that the startup-config is blank. If the switch has previously been provisioned, this can be accomplished by executing a 'write erase' followed by a 'reload' command. Remember not to save the running config when requested.

## Installation

How to install or setup the project for use.

The following activities are required for setup:
* Build an Ubuntu VM instance
* Install ISC DHCP server
* Install Apache2 Web server
* Install Node.js

The Ubuntu server must be reachable from the subnet where the device is to be provisioned.

Follow these steps to config the solution and start the service:

1. Create a DHCP scope with Option 67 defined in "/etc/dhcp/dhcpd.conf"

2. Copy ZTP.py and IBNS2.cfg into "/var/www/html"

3. Place the csv2json.py and serial-ip.csv files in a common directory.

4. Run the shell script, "start-json-server.sh" to start the Node.js service.

## Documentation

Pointer to reference documentation for this project.

For more informaiton on Zero Touch Provisioning and Lifecycle Programmability with IOS XE 16.9, please refer to the following documents...

* [Cisco IOS XE Progammability - Automating Device Lifecycle Management](https://www.cisco.com/c/dam/en/us/products/collateral/enterprise-networks/nb-06-ios-xe-prog-ebook-cte-en.pdf)
* [ZTP in IOS XE 16.9 Programmability Guide](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/prog/configuration/169/b_169_programmability_cg/zero_touch_provisioning.html)
* [Guest Shell with IOx](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/prog/configuration/169/b_169_programmability_cg/guest_shell.html)
* [Identity Based Network Services 2.0](http://www.cisco.com/go/ibns)

## License

Provided under Cisco Sample Code License, for details see [LICENSE](./LICENSE.md)

## Code of Conduct

Our code of conduct is available [here](./CODE_OF_CONDUCT.md)

## Contributing

See our contributing guidelines [here](./CONTRIBUTING.md)

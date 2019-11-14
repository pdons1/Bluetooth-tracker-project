# Digital-Terrain-Mapping-Bluetooth

Release Date: Jul 2019<br />

### CREDITS
Created by Egor Fedorov and uploaded to GitHub in 2015, his code was used as a reference for the code we have created. The code acts as a wrapper for the bluetoothctl utility. The original code written by Fedorov had the ability to pair with available devices and separately identify already paired devices. When writing our code we left out these additional features. Thus, simplifying our code in order to only pick up surrounding devices, display their unique identifiers and attach their signal to a timestamp. In Fedorov’s original code, the scan took place for a set amount of time, only scanning once and did not display the data as it was being collected. We revamped the codes capabilities by enabling it to run continuously, scanning through iterations for a set amount of time and returning the results. This allows us to more accurately attach a time to the scan in which the device was found.

### FUTURE WORK
* Add a component to the code for a GPS to read the location of the device and output the longitude and latitude. 
* Convert the code into the latest version of Python3. The program is currently written in Python 2.7 and will retire on January 1, 2020.
* Create a central server for data to be sent to once received on a mobile node.
* Create a case capable of easily disguising the Raspberry Pi and its components in the field.
* Eliminate duplicates in the discovered devices.
* Boot the code upon powering on the Raspberry Pi. This allows for the avoidance of using a monitor to start the program.

## BUILD PLAN

### DEPENDENCIES
- Python 2.7

### PREPARING FOR CONFIGURATION
Bluetooth is now supported in most modern computers by default. If your computer does not support Bluetooth, you can easily connect a USB Bluetooth Dongle to enable compatibility. There are several packages necessary to utilizing bluetooth, install these if you are unsure of your systems capabilities: bluetooth, bluez and bluetoothctl on Debian. Depending on the type of device, you may need to install other packages.
You can check if your bluetooth is enabled by entering in the terminal: systemctl status bluetooth
If it is not, enter: systemctl start bluetooth
Most devices will stay ready to pair for roughly three minutes. After three minutes, they may need to be readied again.

### GPS MONITORING ADD ON CONFIGURATION
Utilizing the GlobalSat BU-353S4 USB GPS Receiver we looked into acquiring the longitude and latitude of the device. This information is helpful in cases where the device is left alone without an operator. 
We begin by locating the device file that is created when the GPS Receiver is connected to the computer. Before plugging the receiver into the system, open a file browser and navigate to the /dev/ folder. Once you have opened the folder, plug the GPS Receiver into one of the USB ports on your system. A new device file should upload into the folder, named something similar to “ttyUSB0”.
Next, install the pyserial 2.7 module by entering in the terminal: sudo pip install pyserial==2.7. We use version 2.7 to avoid compatibility issues for Python2, the newer versions use primarily Python3.
If your device file was named differently than “ttyUSB0”, change the following lines of code to match your requirements.

This is an optional addition to the code, comment out lines 8-22 and uncomment lines 25-28 and line 130 if you would like to use the user inputted location display.

### BLUETOOTHCTL
Bluetoothctl is the command used in the terminal to connect the system to a device. It provides several options for pairing, blocking, controlling, and trusting. The function we are interested in is its ability to list nearby devices. In its current version, bluetoothctl lists the MAC address and possibly the name given to the device by its user. In our case, the MAC address is the unique identifier we are looking for in order to track someone in the digital realm. 
Since bluetoothctl is a command executed by directly inputting it into the terminal, we needed to make it into an editable code capable of being run through python. This is useful in order to manipulate and collect the data returned through sniffing. Through research, a code was discovered that accomplished similar objectives.

### EXECUTION
Following the download of our code from github and installing all necessary packets and modules listed above, the code is executed in the terminal by entering: sudo python bluetoothcontrol.py. You must run the sudo command in order to get access to the port where the GPS Receiver is connected to. The default program runs each scan iteration for three seconds once bluetoothctl has started. This can be manipulated by changing the following lines of code: 117&118.

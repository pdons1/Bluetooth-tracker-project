import time
import pexpect
import subprocess
import sys
import re
import datetime
import os
import serial

ser = serial.Serial('/dev/ttyUSB0', 4800, timeout=5)

while 1:
	line = ser.readline()
	splitline = line.split(',')

	if splitline[0] == '$GPGGA':
		latitude = line[2]
		latDirec = line[3]
		longitude = line[4]
		longDirec = line[5]
		print line
		break

global clock
#global location
#prompt = '> '
#print("Please enter location.")
#location = raw_input(prompt)

class BluetoothctlError(Exception):
    """This exception is raised, when bluetoothctl fails to start."""
    pass

class Bluetoothctl:
    """A wrapper for bluetoothctl utility."""

    def __init__(self):
        self.child = pexpect.spawn("bluetoothctl", echo = False)

    def get_output(self, command, pause = 0):
        """Run a command in bluetoothctl prompt, return output as a list of lines."""
        self.child.send(command + "\n")
	clock = []
	clock.append(os.system("date"))
	print("*************"*2)
        time.sleep(pause)
        start_failed = self.child.expect(["bluetooth", pexpect.EOF])

        if start_failed:
            raise BluetoothctlError("Bluetoothctl failed after running " + command)

        return self.child.before.split("\r\n")

    def start_scan(self):
        """Start bluetooth scanning process."""
        try:
            self.get_output("scan on")
        except BluetoothctlError, e:
            print(e)
            return None

    def make_discoverable(self):
        """Make device discoverable."""
        try:
            self.get_output("discoverable on")
        except BluetoothctlError, e:
            print(e)
            return None

    def parse_device_info(self, info_string):
        """Parse a string corresponding to a device."""
        device = {}
        block_list = ["[\x1b[0;", "removed"]
        string_valid = not any(keyword in info_string for keyword in block_list)

        if string_valid:
            try:
                device_position = info_string.index("Device")
            except ValueError:
                pass
            else:
                if device_position > -1:
                    attribute_list = info_string[device_position:].split(" ", 2)
		    ts = time.time()
		    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                    device = {"Mac Address:": attribute_list[1],"Name:": attribute_list[2]}
                    
        return device

    def get_available_devices(self):
        """Return a list of tuples of paired and discoverable devices."""
        try:
            out = self.get_output("devices")
        except BluetoothctlError, e:
            print(e)
            return None
        else:
            available_devices = []
            for line in out:
                device = self.parse_device_info(line)
                if device:
                    available_devices.append(device)

            return available_devices

    def get_device_info(self, mac_address):
        """Get device info by mac address."""
        try:
            out = self.get_output("info " + mac_address)
        except BluetoothctlError, e:
            print(e)
            return None
        else:
            return out

if __name__ == "__main__":
	loop_iter = 3 #Number of times to check, each will take scan_time seconds to complete
	scan_time = 3 #Number of seconds to scan for
	print("Initiating bluetooth...")
	print("Ready!")
	for i in range(0,loop_iter):
		bl = Bluetoothctl()
		bl.start_scan()
		print("Scanning for " + str(scan_time) + " seconds...")
		print("Iterating through " +str(loop_iter) + " scan sessions...")
		for i in range(0, scan_time):
			print(i)
			time.sleep(1)
		print("***************"*2)
		#print "The devices location is: ", location
		for item in bl.get_available_devices():
				for key in item:
					print(key + ' ' + item[key])
				print("---------------"*2)

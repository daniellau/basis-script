#! /usr/bin/python

__author__ = "jacobbjones"

import subprocess
import os

def edittext(text,value,line):
	f = open(text,"r")
	contents = f.readlines()
	f.close()
	
	if line == 000:
		contents.append(value)
	else:
		contents[line] = value

	f = open(text, "w" )
	contents = "".join(contents)
	f.write(contents)
	f.close()


def uuid():
	text = "/etc/permissions.local"
	value = "\n/usr/sbin/uuidd uuidd:uuidd 6755\n"
	line = 32
	
	try:
		subprocess.call(['uuidgen -t'])
	except OSError:
		print ('sapconfpackage not installed') 
	else:
		edittext(text,value,line)
		subprocess.call(("insserv uuidd"),shell=True)
		subprocess.call(("/etc/init.d/uuidd start"),shell=True)

def users():
	text = "/etc/ssh/sshd_config_test"
	value = "\nAllowUsers"
	line = 000

	username = ["jconnolly","jjones","narmstrong4","awong","dlau"]
	passw = "Basis4me!"

	for i in range(0,5):
		subprocess.call(("useradd -m -g wheel -p "+passw+" -s /bin/bash "+username[i]),shell=True)
		value = value +" "+username
	
	edittext(text,value,line)



text = "/etc/ntp.conf"
value = ("\nserver 0.us.pool.ntp.org \nserver 1.us.pool.ntp.org\nserver 2.us.pool.ntp.org\nserver 3.us.pool.ntp.org\n" )
line = 27

edittext(text,value,line)
subprocess.call(("rcntp start"),shell=True)
uuid()
subprocess.call(("/etc/init.d/nscd stop"),shell=True)
subprocess.call(("/etc/init.d/boot.sysstat start"),shell=True)



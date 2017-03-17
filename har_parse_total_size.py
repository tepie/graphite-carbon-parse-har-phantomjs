#!/usr/bin/python


import re
import sys
import time
import socket
import json

CARBON_SERVER = '192.168.0.38'
CARBON_PORT = 2003
DELAY = 60

def run(sock, delay):
	"""Make the client go go go"""
	while True:
		now = int(time.time())
		lines = []

		f1 = open(sys.argv[1],'r')

		json_har = json.loads(f1.read())

		total_body_size = 0

		for entry in json_har['log']["entries"]:
			body_size = entry["response"]["bodySize"]

			total_body_size = total_body_size + body_size

		f1.close()

		
		on_load = json_har['log']["pages"][0]["pageTimings"]["onLoad"]
		
		lines.append("networking.har.total_body_size %s %d" % (total_body_size, now))
		lines.append("networking.har.on_load %s %d" % (on_load, now))
		#lines.append("system.loadavg_15min %s %d" % (loadavg[2], now))
		message = '\n'.join(lines) + '\n' #all lines must end in a newline
		print "sending message"
		print '-' * 80
		print message
		sock.sendall(message)
		time.sleep(delay)

def main():
	"""Wrap it all up together"""
	delay = DELAY
	
	sock = socket.socket()
	try:
		sock.connect( (CARBON_SERVER, CARBON_PORT) )
	except socket.error:
		raise SystemExit("Couldn't connect to %(server)s on port %(port)d, is carbon-cache.py running?" % { 'server':CARBON_SERVER, 'port':CARBON_PORT })

	try:
		run(sock, delay)
	except KeyboardInterrupt:
		sys.stderr.write("\nExiting on CTRL-c\n")
		sys.exit(0)

if __name__ == "__main__":
	main()

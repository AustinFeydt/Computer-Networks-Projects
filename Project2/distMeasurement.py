
#TO RUN: type sudo python distMeasurement.py
import time
import socket
import struct

#Reads file of IPs and puts them into a python list
targets = open("targets.txt")
ip_list = targets.read().splitlines()
print "The following IP addresses will be tested:"

for x in ip_list:
	print x
print "\n"

#creates a UDP socket over the default address family
udp = socket.getprotobyname('udp')
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)
#creates a ICMP socket over the default address family
icmp = socket.getprotobyname('icmp')
rcv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)

#Constant TTL and port number for each datagram sent out through the UDP socket
ttl = 32
port = 50005

#Loops through each IP in list
for x in ip_list:
	ip = x

	##message of about 1480 bytes of data
	message = """
	abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz
	abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz
	abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz
	abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz
	abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz
	abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz
	abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz
	abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz
	abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz
	abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz
	abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz
	abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz
	abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz
	abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz
	abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz
	abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz
	abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz
	abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz
	abcdefghijklmnopqrstuvwxyz
	"""
	
	print "Sending packet to",ip 
	
	#Changes TTL of datagram
	udp_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
	
	#Counter of how many datagrams have been sent out (so we don't get stuck if we get an annoying IP)
	tries = 1
	
	#Sets the timeout of the UDP socket to 3 seconds (to avoid an infinite loop)
	rcv_socket.settimeout(3.0)
	
	#Each packet gets sent a maximum of 3 times
	while tries < 4:
		
		#timestamp of when packet is sent
		time_start = time.time()
		#Sends datagram with custom TTL to current IP and constant port number
		udp_socket.sendto(message, (ip,port))
		print time_start

		try:
			#read data from receive ICMP socket
			data, address = rcv_socket.recvfrom(1024)

			#Timestamp of when packet received (if it is even received)
			time_stop = time.time()
			
			#If the address returned matches the IP
			if (address[0] == x):
				
				#parses the original header to get back the final TTL and protocol
				final_ttl, protocol = struct.unpack("!xxxxxxxxBBxxxxxxxxxx", data[28:48])
				print "The number of hops to this IP is: ",ttl - int(final_ttl), " hops" 
				print "The RTT of the packet is: ", time_stop-time_start," ms"
				
				"""parses header to get the total length of the datagram. 
				We subtract 28 bytes because 20 represent the new IP header, and 8 represent the ICMP header.
				This leaves us with the 20 byte original header and some of the original payload
				"""
				icmp_length = struct.unpack("!xxH", data[0:4])
				print "The number of bytes from the original datagram is:", icmp_length[0] - 28," bytes\n"
				break

		#deals with the case that no data comes into the receiving socket	
		except socket.timeout:
			print "timeout"
			tries = tries + 1
			if tries == 4:
				print "FAILED TO CONNECT. MOVING ON TO NEXT IP\n"
udp_socket.close()
rcv_socket.close()
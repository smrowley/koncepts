from email import utils


import os
import socket

def get_file_contents(file_path):
    if os.path.isfile(file_path):
        #open text file in read mode
        text_file = open(file_path, "r")
 
        #read whole file to a string
        data = text_file.read()
    
        #close file
        text_file.close()
    
        return data
    else:
        return "N/A"

def get_ip_address(hostname):
    return socket.gethostbyname(hostname)
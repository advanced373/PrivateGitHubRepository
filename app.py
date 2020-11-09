import socket
import subprocess
import os
import pwd
import pdb
import sys
import traceback
from threading import Thread
from library import get_username
from client_thread import client_threading
sockfd=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockfd.bind(('',12348))
sockfd.listen(4)
print("My echo server is listening on port:12348")
while True:
    conn, client_addr = sockfd.accept()
    print("Conencted with"+client_addr[0])
    try:
        Thread(target=client_threading,args=(conn,client_addr)).start()
    except:
        print("Thread did not start.")
        traceback.print_exc()
sockfd.close()

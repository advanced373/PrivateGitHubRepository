import socket
import subprocess
import os
import pwd
import pdb
from library import get_username
from glob import glob
def client_threading(conn, client_addr):       
    while True:
        payload = conn.recv(1024)
        try:
            value= repr(payload).split("::")
            value[0]=value[0].replace("b'","")
            pat="/home/pi/backup"
            if os.path.isdir("/home/pi/backup" == False) :
                os.system("systemctl stop backup.timer")
                os.system("systemctl disable backup.timer")
                os.system("systemctl start backup2.timer")
                os.system("systemctl enable backup2.timer")
                pat="media/pi/786B-6C443"
                os.chdir("media/pi/786B-6C443")
                print("file error")
            if value[0] == "register" :
                pwd.getpwnam(value[1])
                conn.sendto("no!".encode('ascii'),client_addr)                
            elif value[0] == "delete" :
                if len(value) != 2 :
                    raise Exception("Sorry")
                value[1]=value[1].replace("\\n'","")
                conn.sendto(value[1].encode('ascii'),client_addr)
                command="grep -c '^"+value[1].rstrip()+":' /etc/passwd"
                t=os.popen(command).readlines()
                if t == ["0\n"] :
                    raise Exception()
                os.system("sudo userdel "+value[1])
                os.system("sudo rm -r /home/pi/backup/"+value[1])
                conn.sendto("ok".encode('ascii'),client_addr)
            elif value[0] == "init" :
                if len(value) != 4 :
                    raise Exception("Sorry")
                path="/home/pi/backup/"
                path=path+value[1]
                if os.path.isdir(path) == True:
                    value[2]=value[2].replace("'","")
                    command="backup/"
                    command=command+ value[1]
                    os.chdir(command)
                    c="sudo mkdir "
                    c=c+value[2]
                    c=c+".git"
                    p=value[2]+".git"
                    os.system(c)
                    os.chdir(p)
                    command="sudo git init --bare "
                    os.system(command)
                    conn.sendto('ok'.encode('ascii'),client_addr)
                    os.chdir('/home/pi')
                else :
                    conn.sendto('no'.encode('ascii'),client_addr)
            elif value[0] == "log" :
                if len(value) !=2 :
                    raise Exception("Sorry")
                value[1]=value[1].replace("'","")
                print(value[1])
                path="/home/pi/backup/"
                path=path+value[1]
                path=path+"/*/"
                t=glob(path)
                result=""
                for v in t:
                    print(v)
                    m=v.split('/')
                    t=m[5].split('.')
                    result=result+t[0]
                    result=result+';'
                if result == "" :
                    conn.sendto("no".encode('ascii'),client_addr)
                conn.sendto(result.encode('ascii'),client_addr)
                print(result)
            elif value[0] == "login" :
                if len(value) != 3 :
                    conn.sendto("Wrong format!".encode('ascii'),client_addr)
                    continue
                command="grep -c '^"+value[1].rstrip()+":' /etc/passwd"
                t=os.popen(command).readlines()
                if t != ["0\n"] :
                    print(value[2])
                    value[2]=value[2].replace("'","")
                    command="openssl passwd -salt 'salt' "
                    print(value[2])
                    command=command+value[2]
                    password=os.popen(command).readlines()
                    password[0]=password[0].replace("\n","")
                    print(password[0])
                    print(get_username(value[1]))
                    if get_username(value[1]) == password[0] :
                        conn.sendto("ok".encode('ascii'),client_addr)
                    else:
                        conn.sendto("no".encode('ascii'),client_addr)
                else:
                    conn.sendto("ok".encode('ascii'),client_addr)
            elif len(value) == 1 :
                value[0]=value[0].replace("\\n'","")
                if value[0] == "exit":
                    conn.sendto("User disconected!".encode('ascii'),client_addr)
                    conn.close()
                    break
                else :
                    raise Exception("Wrong format!")
            else:
                raise Exception("Wrong format!")
        except KeyError as err :
            value[2]=value[2].replace("'","")
            conn.sendto(value[2].encode('ascii'),client_addr)
            conn.sendto(value[1].encode('ascii'),client_addr)
            os.system("sudo /usr/sbin/useradd -m -d /home/pi/backup/"+value[1]+ " -p $(openssl passwd -salt 'salt' "+value[2]+" ) " +value[1])
            conn.sendto("ok".encode('ascii'),client_addr)
        except Exception as error:
            if value[0] == "delete" :
                conn.sendto("no".encode('ascii'),client_addr) 
                continue
            conn.sendto(error.args[0].encode('ascii'),client_addr)
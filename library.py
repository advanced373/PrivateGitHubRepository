import os
def get_username(username):
    com="sudo cat /etc/shadow | grep '^"
    com=com+username
    com=com+"'"
    command=os.popen(com).readlines()
    password=command[0].split(':')
    return password[1]
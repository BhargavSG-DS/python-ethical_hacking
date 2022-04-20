import paramiko
import scp

ssh_client = paramiko.SSHClient()

ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh_client.connect("web.sourceforge.net", username="barrrygadhiya", password="bat%rox@74")
print('[+] Authenticating against web.sourceforge.net')

scp = scp.SCPClient(ssh_client.get_transport())

scp.put("D:/ethicalhacking_python/IEhijack.py")
print('[+] File is uploaded')

scp.close()

print("[+] Closing The Socket")
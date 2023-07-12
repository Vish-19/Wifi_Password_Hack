import subprocess
import re
key = {}
command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True, shell=True).stdout.decode()
profile_names = (re.findall("All User Profile     :(.*)\r", command_output))
name = 'Edil'
profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output = True, shell=True).stdout.decode()
password = re.search("Key Content            : (.*)\r", profile_info)
print(profile_names)
# password = password[1]
# key[name] = password
# print(key)
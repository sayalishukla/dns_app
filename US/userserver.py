#Sayali Shukla

from flask import Flask, request
import requests
import socket

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello world!'

@app.route('/fibonacci', methods=['GET'])
def fibonacci():

    data = request.args
    print(data)
    # Check for the parameters are missing,
    if 'hostname' not in data \
        or 'fs_port' not in data \
        or 'number' not in data\
        or 'as_ip' not in data \
        or 'as_port' not in data:
            return "Bad Request",400

    # Querying authoritative DNS server to get IP address of the given hostname
    UDP_IP = data.get('as_ip')
    UDP_PORT = int(data.get('as_port'))

    str_msg = 'TYPE=A\nNAME={0}\n'.format(data.get('hostname'))
    MESSAGE = bytes(str.encode(str_msg))
    clientSock = socket.socket(socket.AF_INET,  # Internet
                               socket.SOCK_DGRAM)  # UDP
    clientSock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    modifiedMessage, serverAddress = clientSock.recvfrom(2048)
    dec_msg = modifiedMessage.decode()
    print(dec_msg)
    fs_server = None
    for l in dec_msg.split():
        if "VALUE" in l:
            fs_server = l.split("=")[1]

    # Create a url from retirved host's  IP address
    server_url = f'http://{fs_server}:{data.get("fs_port")}/fibonacci?number={data.get("number")}'
    resp = requests.get(server_url)
    print(resp)
    return resp.text, resp.status_code


app.run(host='0.0.0.0',
        port=8080,
        debug=True)

# http://0.0.0.0:8080/fibonacci?hostname=fibonacci.com&fs_port=9090&number=3&as_ip=0.0.0.0&as_port=53533

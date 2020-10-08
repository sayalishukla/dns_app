#Sayali Shukla
import socket

from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello world!'

'''
# HTTP PUT request at path “/register”
fibo_data ={
        "hostname":"fibonacci.com",
        "ip": "0.0.0.0",
        "as_ip": "0.0.0.0",
        "as_port": "53533"
    }
    resp1 = requests.put(f"http://0.0.0.0:9090/register", data=fibo_data)
    print(resp1)
    
'''

# Registration to Authoritative Server
@app.route('/register', methods=['PUT'])
def register():
    jsonobj = request.form

    hostname = jsonobj.get('hostname')
    fs_ip = jsonobj.get('ip')
    print(hostname,fs_ip)

    # UDP_IP = as_ip  & UDP_PORT = as_port
    UDP_IP = jsonobj.get('as_ip')
    UDP_PORT = int(jsonobj.get('as_port'))

    str_msg = 'TYPE=A\nNAME={0}\nVALUE={1}\nTTL=10\n'.format(hostname,fs_ip)
    MESSAGE = bytes(str.encode(str_msg))

    clientSock = socket.socket(socket.AF_INET,  # Internet
                               socket.SOCK_DGRAM)  # UDP
    clientSock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    modifiedMessage, serverAddress = clientSock.recvfrom(2048)
    dec_msg = modifiedMessage.decode()
    print("resp**" + dec_msg)

    # HTTP response with code 201.
    if dec_msg:
        return "OK", 201
    else:
        return "Internal Server Error", 500

# Get Fibonacci number for the sequence number X
@app.route('/fibonacci', methods=['GET'])
def get_fibo_no():
    #get input
    data = request.args
    try:
        n = int(data.get('number'))
        print(n)
    except:
        return "Bad Format", 400
    ans = fibonacci(n)
    print(ans)
    if ans == -1:
        return "Bad Format", 400
    return str(ans), 200

# calculate fibonacci
def fibonacci(n):
    a = 0
    b = 1
    if n <= 0:
        return -1
    elif n == 1:
        return b
    else:
        for i in range(2,n):
            c = a + b
            a = b
            b = c
        return b

app.run(host='0.0.0.0',
        port=9090,
        debug=True)


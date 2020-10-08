#Sayali Shukla
import socket

UDP_IP = "0.0.0.0"
UDP_PORT = 53533

def UDPServer():

    serverSock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP
    serverSock.bind((UDP_IP, UDP_PORT))
    print(f"listening on {UDP_PORT}")
    while True:

        data, clientAddress = serverSock.recvfrom(2048) # buffer size is 1024 bytes
        # Decoding data
        modifiedMessage = data.decode().upper()
        print(modifiedMessage)

        # Registration requests to pair hostnames to IP
        if "NAME" in modifiedMessage and "VALUE" in modifiedMessage\
                and "TYPE" in modifiedMessage\
                and "TTL" in modifiedMessage:
            with open("hostname.txt",'a') as fp:
                fp.writelines(modifiedMessage)

        # Respose to DNS queries from clients
        elif "TYPE" in modifiedMessage and "NAME" in modifiedMessage:
            print(modifiedMessage)
            type, name = modifiedMessage.split()
            resp = "TYPE=A\n"
            with open("hostname.txt",'r') as fp:
                for line in fp:
                    if name in line:
                        resp += line + next(fp) + next(fp)
                        break
            modifiedMessage = resp
        serverSock.sendto(modifiedMessage.encode(),clientAddress)
        print("received message: %s" % data)

if __name__ == "__main__":
    UDPServer()
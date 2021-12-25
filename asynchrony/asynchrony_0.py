import socket

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server_socket.bind(("localhost",5001))
server_socket.listen()


while True:
    client_socket, adress = server_socket.accept()
    print("Connection from", adress)
    while True:
        requests = client_socket.recv(4096)
        if not requests:
            break
        else:
            responce = "Hell world\n".encode()
            client_socket.send(responce)

    client_socket.close()





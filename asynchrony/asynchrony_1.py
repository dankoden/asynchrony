import socket
from select import select

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server_socket.bind(("localhost",5000))
server_socket.listen()
to_monitor = []

# Распределили функционал программы по функциям , добавили select теперь наш серевер в одном потоке,
# может отвечать сразу двум клиентским сокетам , пока один набирает а другой подал запрос на соеденение 

def accept_connection(server_socket):
        client_socket, adress = server_socket.accept()
        print("Connection from", adress)
        send_message(client_socket)

        to_monitor.append(client_socket)

def send_message(client_socket):

        requests = client_socket.recv(4096)

        if requests:
            responce = "Hell world\n".encode()
            client_socket.send(responce)

        else:
            client_socket.close()

def event_loop():

    while True:
        ready_to_read, _ ,_ = select(to_monitor,[],[]) # Читает файлы переданные в нее и возвращает список готов файлов для записи
        for sock in ready_to_read:
            if sock is server_socket:
                accept_connection(sock)
            else:
                send_message(sock)

if __name__ == "__main__":
    to_monitor.append(server_socket)
    event_loop()
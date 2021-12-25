import socket
from select import select

tasks = [] # список генераторов функций

to_read = {} # Итератор котторый будут скормлен ф-ии select
to_write = {} # Итератор котторый будут скормлен ф-ии select

def server():

    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    server_socket.bind(("localhost",5004))
    server_socket.listen()


    while True:

        yield ("read", server_socket) # Создаем генератор который вернет кортеж, далее он будет распакован при создании итератора для select
        client_socket, adress = server_socket.accept()

        print("Connection from", adress)
        tasks.append(client(client_socket))


def client(client_socket):
    while True:

        yield ("read", client_socket)
        requests = client_socket.recv(4096)

        if not requests:
            break
        else:
            responce = "Hell from localhost server\n".encode()

            yield ("write", client_socket)
            client_socket.send(responce)

    client_socket.close()

def event_loop():

    while any([tasks,to_read,to_write]):

        while not tasks:

            ready_to_read, ready_to_write, _ = select(to_read, to_write, []) # Делает выборку готовых для записи или чтения файлов

            for sock in ready_to_read:
                tasks.append(to_read.pop(sock)) # Добавляем в tasks генератор

            for sock in ready_to_write:
                tasks.append(to_write.pop(sock)) # Добавляем в tasks генератор
        try:
            task = tasks.pop(0)
            reason , sock =  next(task) # Запускаем генератор 1 из списка tasks и удаляем его одтуда

            if reason == "write":
                to_write[sock] = task # Заолняем итератор для select
            if reason == "read":
                to_read[sock] = task # Заолняем итератор для select
        except StopIteration:
            print("DONE")


tasks.append(server())# Запустили ф-ю  создания сервера, она же является генератором первыйм добавленным в список tasks
event_loop()# Заупскаем основной цикл событий
import socket
import selectors


# Используем модуль Selectors, его тоже нужно подкармливать обьэктами за которыми
# нужен мониторинг и ответ когда же они статус свободны для записи или чтения
# для этго используется специальный метод register, принимает 3 параметра
# Обьэкт за которым нужно следить, для какого режима нам нужен обьэкт и данные связяанные с этим обьэктом
# тут мы использовали callback - это обьэкт который нам вернул метод select() у нашего selectors.DefaultSelector()
# метод select() - возвращает кортеж с двух елементов , первым элементом является клюс которые являеется
# обьэктом класса , которые мы создали при регистрации (метод register) и у ключа есть параметры все те что
# мы передавали при создании (метод register). Если обьэкт готов к чтению то selector его в значении key и
# нам нужно его запустить с помощью параметров которые которые были переданы при создании

selector = selectors.DefaultSelector()

def serever():
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    server_socket.bind(("localhost",5002))
    server_socket.listen()

    selector.register(fileobj=server_socket,events=selectors.EVENT_READ,data=accept_connection)

def accept_connection(server_socket):
    client_socket, adress = server_socket.accept()
    print("Connection from", adress)

    selector.register(fileobj=client_socket,events=selectors.EVENT_READ,data=send_message)

def send_message(client_socket):

        requests = client_socket.recv(4096)

        if requests:
            responce = "Hell world\n".encode()
            client_socket.send(responce)

        else:
            selector.unregister(client_socket) # сняли с регистрации
            client_socket.close() # закрыли сокет

def event_loop():
    while True:
        events = selector.select()  # (key,events)
        for key,_ in events:
            callback = key.data
            callback(key.fileobj)



if __name__ == "__main__":
    serever()
    event_loop()
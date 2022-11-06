import socket
from _thread import *
import drinksSDK

is_local = True


def getCurrentDrinks():
    drinks = drinksSDK.get_drinks(True)

    names = ['', '', '']
    portions = ['', '', '']

    for item in drinks:
        names[item[1]-1] = item[2]
        portions[item[1]-1] = item[3]

    return names, portions


def handleData(data, connection):

    if not data.isnumeric() or len(data) != 1:
        return False

    data = int(data)

    if data == 1:
        drinksSDK.refill_portion(1, 4, 'buttonLink')
        return f'{data} refilled'

    elif data == 2:
        drinksSDK.refill_portion(2, 4, 'buttonLink')
        return f'{data} refilled'

    elif data == 3:
        drinksSDK.refill_portion(3, 4, 'buttonLink')
        return f'{data} refilled'

    elif data == 4:
        while True:
            connection.send(
                'Enter drink data seperated by //: [name//portions//buttonLink]'.encode())
            response = connection.recv(2048).decode('utf-8').split('//')

            try:
                drinksSDK.add_drink(response[0], int(
                    response[1]), int(response[2]))
                return f'Drink added'
            except Exception:
                connection.send(
                    'Something went wrong. Please try again.'.encode())

    elif data == 5:
        while True:
            connection.send(
                'Enter data to change button: [name//button] '.encode())
            response = connection.recv(2048).decode('utf-8').split('//')

            print(response)

            try:
                drinksSDK.update_buttonlink(response[0], int(response[1]))
                return f'Button changed'
            except Exception:
                connection.send(
                    'Something went wrong. Please try again.'.encode())

    elif data == 6:
        while True:
            connection.send(
                'Enter data to delete drink: [name or id] '.encode())
            response = connection.recv(2048).decode('utf-8').split('//')

            try:
                drinksSDK.delete_drink(response[0], response[1])
                return f'Drink deleted'
            except Exception:
                connection.send(
                    'Something went wrong. Please try again.'.encode())

def multi_threaded_client(connection):

        drinks, portions = getCurrentDrinks()

        init_msg = f'''
        CONNECTION SUCCESFULL - Welcome to Restocking for TenderBot

        What would you like to restock?

        [1] {drinks[0]}     [Portions Left]: {portions[0]}
        [2] {drinks[1]}     [Portions Left]: {portions[1]}
        [3] {drinks[2]}     [Portions Left]: {portions[2]}

        [4] Add Drink
        [5] Set Button
        [6] Remove Drink
 
        '''
        connection.send(init_msg.encode())

        while True:

            data = connection.recv(2048).decode('utf-8')
            if not data or data == 'exit':
                break

            response = handleData(data, connection)

            connection.sendall(str(response).encode())

        connection.close()

def main():

    try:
        ServerSideSocket = socket.socket()
        host = '127.0.0.1' if is_local else '192.168.1.11'
        port = 2222
        ThreadCount = 0

        try:
            ServerSideSocket.bind((host, port))
        except socket.error as e:
            print(str(e))
            ServerSideSocket.close()
        print('RESTOCKING SERVICE FOR TENDERBOT IS RUNNING')
        ServerSideSocket.listen(5)

        while True:
            Client, address = ServerSideSocket.accept()
            print(f'Connected to: {address[0]} : {address[1]}')
            start_new_thread(multi_threaded_client, (Client,))
            ThreadCount += 1
            print('Thread Number: ' + str(ThreadCount))

    except Exception as e:
        print(e)

    finally:
        ServerSideSocket.close()

if __name__ == '__main__':
    main()

import socket
from _thread import *
import drinksSDK
import pandas as pd

is_local = False

host = '127.0.0.1' if is_local else '192.168.12.52'
port = 14000

validOptions = ['1', '2', '3', '4', '5', '6', '7', '8']

def getCurrentDrinks():
    drinks = drinksSDK.get_drinks(True)

    names = ['', '', '']
    portions = ['', '', '']

    for item in drinks:
        names[item[1]-1] = item[2]
        portions[item[1]-1] = item[3]

    return names, portions

def addNumbers(words, numToUse):

    longest = len(max(words, key=len)) + 1
    newWords = []

    for word in words:

        length = len(word)
        spaces = longest - length
        newWord = word + ':' + ' ' * spaces

        newWord += str(numToUse)
        newWords.append(newWord)

    return newWords


def handleData(data, connection):

    if not data.isnumeric() or len(data) != 1:
        return False

    data = int(data)

    if data == 1:
        resp = drinksSDK.refill_portion(1, 4, 'buttonLink')
        if resp:
            return 'Portion successfully added'
        else:
            return 'Portion not added'

    elif data == 2:
        resp = drinksSDK.refill_portion(2, 4, 'buttonLink')
        if resp:
            return 'Portion successfully added'
        else:
            return 'Portion not added'    

    elif data == 3:
        resp = drinksSDK.refill_portion(3, 4, 'buttonLink')
        if resp:
            return 'Portion successfully added'
        else:
            return 'Portion not added'

    elif data == 4:
        while True:
            init_msg = getInitMsg()
            connection.send(f'{init_msg} \n\nEnter drink data seperated by //: [name//portions//buttonLink]'.encode())
            response = connection.recv(2048).decode('utf-8').split('//')

            try:
                resp = drinksSDK.add_drink(response[0], int(response[1]), int(response[2]))
            except Exception as e:
                connection.send('Invalid data. Please try again.\n'.encode())
                continue
            
            if resp:
                return 'Drink successfully added'
            else:
                return 'Drink not added'

    elif data == 5:
        while True:
            init_msg = getInitMsg()
            connection.send(
                f'{init_msg} \n\nEnter data to change button: [name//button]'.encode())
            response = connection.recv(2048).decode('utf-8').split('//')

            print(response)

            try:
                resp = drinksSDK.update_buttonlink(response[0], int(response[1]))
            except Exception:
                connection.send('Something went wrong. Please try again.'.encode())
                continue
            
            if resp:
                return 'Button successfully changed'
            else:
                return 'Button not changed'

    elif data == 6:
        init_msg = getInitMsg()
        while True:
            connection.send(
                f'{init_msg} \n\nEnter data to delete drink: [name or id] '.encode())
            response = connection.recv(2048).decode('utf-8').split('//')

            try:
                drinksSDK.delete_drink(response[0], response[1])
                return f'Drink deleted'
            except Exception:
                connection.send(
                    'Something went wrong. Please try again.'.encode())

    elif data == 7:
        drinks = drinksSDK.get_drinks(False)
        drinks_str = 'DRINKS IN THE DATABASE:\n\n'

        df = pd.DataFrame(drinks, columns=['ID', 'BUTTONS', 'NAME', 'PORTIONS', 'LAST USED'])
        drinks_str =  drinks_str + str(df)
        
        drinks_str += '\nPress enter to continue'
        connection.send(drinks_str.encode())
        resp = connection.recv(2048).decode('utf-8')
        return ''

    
    elif data == 8:
        return 'exit'

def getInitMsg():

    drinks, portions = getCurrentDrinks()

    init_msg = f'''
    CONNECTION SUCCESFULL - Welcome to Restocking for TenderBot

    Instantly refill a portion of a drink:

    [1] {drinks[0]}     [Portions Left]: {portions[0]}
    [2] {drinks[1]}     [Portions Left]: {portions[1]}
    [3] {drinks[2]}     [Portions Left]: {portions[2]}

    

    [4] Add Drink
    [5] Set Button
    [6] Remove Drink
    [7] List All Drinks
    [8] Exit

    Press Enter to Refresh

    '''

    return init_msg

def multi_threaded_client(connection, addr):
    global ThreadCount

    init_msg = getInitMsg()
    connection.send(init_msg.encode())

    while True:

        

        data = connection.recv(2048).decode('utf-8')
        if not data or data == '8':
            break

        if data in validOptions:
            print(f'[{addr[0]} : {addr[1]}] - Is making a change')
            response = handleData(data, connection)
            print(f'[{addr[0]} : {addr[1]}] - Made a change\n')
        elif data == ' ':
            response = 'Refreshed'
        else:
            response = 'Invalid option'

        updated_data = f'{getInitMsg()}\n{response}'

        connection.sendall(str(updated_data).encode())

    connection.close()
    print(f'Client: [{addr[0]} : {addr[1]}] has disconnected')
    ThreadCount -= 1
    print(f'Thread Number: {ThreadCount}')

def main():
    global ThreadCount

    try:
        ServerSideSocket = socket.socket()
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
            start_new_thread(multi_threaded_client, (Client, address))
            ThreadCount += 1
            print('Thread Number: ' + str(ThreadCount))

    except Exception as e:
        print(e)

    finally:
        ServerSideSocket.close()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Exiting...')
        exit(0)

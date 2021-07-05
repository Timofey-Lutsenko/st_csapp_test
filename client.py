import socket
import sys

from common.temp_storage import i_know_this_commands as cmds
from common.client_messages import *
from common.config_sample import *


s = socket.socket()
s.connect((IP, PORT))


def main():
    print(welcome_text)
    while True:
        user_data = input(">>:")
        if user_data.lower() == 'stop':
            s.close()
            break
        if user_data.lower() == 'help':
            print(help_text)
            continue
        user_data_list = user_data.split()
        if user_data_list[0] in cmds:
            # Проверка кол-ва аргументов.
            if len(user_data_list) == 2:
                s.send(bytes(user_data, 'utf-8'))
            else:
                print(incorrect_num_of_args)
                continue
        else:
            print(unknown_command)
            continue
        server_data = s.recv(2048)
        print(server_data.decode('utf-8'))


if __name__ == '__main__':
    main()

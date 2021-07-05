import socket
import multiprocessing
import time


from common.fucnctions import *
from common.utils import *
from common.server_messages import *
from common.config_sample import *
from database_controller import conn


def listener(q):
    server_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_s.bind((IP, PORT))
    server_s.listen(CONNECTIONS_LIMIT)
    while True:
        connection, addr = server_s.accept()
        print(f'Connected: {addr}')
        while True:
            try:
                client_data = connection.recv(2048)
                client_data = client_data.decode(ENCODING).split()
                # Постановка задачи.
                if client_data[0] == '-rev' \
                        or client_data[0] == '-ec':
                    task_obj = task_assembler(
                        client_data[0], client_data[1], q)
                    data_to_client = f'The task has been formed ' \
                                     f'and received an ID: ' \
                                     f'{task_obj.task_id}'
                    connection.send(bytes(data_to_client, ENCODING))
                if client_data[0] == '-res':
                    if id_validator(client_data[1]):
                        sql_pattern = """ 
                        SELECT * FROM 'tasks'
                        WHERE task_id = ?
                        """
                        cur = conn.cursor()
                        cur.execute(sql_pattern, (client_data[1], ))
                        curr_result = cur.fetchall()
                        conn.commit()
                        if curr_result[0][3] == 'Done':
                            connection.send(bytes(
                                'Result by ID is: ' +
                                curr_result[0][4], ENCODING
                            )
                            )
                            continue
                        else:
                            connection.send(bytes(
                                status_is_not_ready, ENCODING
                            )
                            )
                            continue
                    else:
                        connection.send(bytes(unknown_id, ENCODING))
                        continue
                # Вызов статуса.
                if client_data[0] == '-s':
                    if id_validator(client_data[1]):
                        sql_pattern = """ 
                        SELECT * FROM 'tasks'
                        WHERE task_id = ?
                        """
                        cur = conn.cursor()
                        cur.execute(sql_pattern, (client_data[1],))
                        curr_result = cur.fetchall()
                        connection.send(bytes(
                            f'Status of task with {client_data[1]} ID is: ' +
                            curr_result[0][3], ENCODING)
                        )
                        continue
                    else:
                        connection.send(bytes(unknown_id, ENCODING))
                        continue
            except ValueError:
                connection.send(b'Incorrect value')


def shepherd(q):
    while True:
        if not q.empty():
            try:
                curr_task = q.get()
                sql_pattern = """ 
                UPDATE tasks SET status = ?
                WHERE task_id = ?"""
                cur = conn.cursor()
                cur.execute(sql_pattern,
                            ('In progress.',
                             f'{curr_task.task_id}')
                            )
                conn.commit()
                if curr_task.task_type == '-rev':
                    # Обновление результата через вызов функции,
                    # преобразующей пользовательские данные.
                    curr_task.result_updater(
                        reverser(curr_task.task)
                    )
                    # Обновление статуса задачи у объекта.
                    curr_task.task_status_updater('Done')
                    # Обновление записи в БД.
                    sql_pattern = """ 
                    UPDATE tasks 
                    SET status = ?, result = ? 
                    WHERE task_id = ?
                    """
                    values = (
                        f'{curr_task.status}',
                        f'{curr_task.result}',
                        f'{curr_task.task_id}')
                    cur = conn.cursor()
                    cur.execute(sql_pattern, values)
                    conn.commit()
                    print(f'Task with ID {curr_task.task_id} '
                          f'completed successfully.')
                if curr_task.task_type == '-ec':
                    curr_task.result_updater(
                        is_even_handler(curr_task.task)
                    )
                    curr_task.task_status_updater('Done')
                    sql_pattern = """ 
                    UPDATE tasks 
                    SET status = ?, result = ? 
                    WHERE task_id = ?
                    """
                    values = (
                        f'{curr_task.status}',
                        f'{curr_task.result}',
                        f'{curr_task.task_id}')
                    cur = conn.cursor()
                    cur.execute(sql_pattern, values)
                    conn.commit()
                    print(f'Task with ID {curr_task.task_id} '
                          f'completed successfully.')
                    continue
            except IndexError:
                print("Order list is empty")


if __name__ == '__main__':
    q = multiprocessing.Queue()
    listener_process = multiprocessing.Process(target=listener, args=(q,))
    listener_process.start()
    shepherd_process = multiprocessing.Process(target=shepherd, args=(q,))
    shepherd_process.start()
    listener_process.join()
    listener_process.join()

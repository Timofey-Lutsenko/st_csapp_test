from collections import deque


from common.temp_storage import *
from database_controller import conn


# Класс "Задача"
# Включает тип задачи, ID, пользовательские данные для работы
# статус выполнения и результат
class Task:
    def __init__(self, task_type, task_id, task_str, status, result):
        self.task_type = task_type
        self.task_id = task_id
        self.task = task_str
        self.status = status
        self.result = result

    # Переопределение оператора сравнения.
    def __eq__(self, other):
        if self.task_id == other:
            return True
        else:
            return False

    # Функция перезаписывающая статус задачи.
    def task_status_updater(self, new_status):
        self.status = new_status

    # Функция перезаписывающая результат.
    def result_updater(self, new_result):
        self.result = new_result


# Функция-конструктор.
def task_assembler(type_of_task, task_str, q):
    task_id = task_id_creator(type_of_task)
    status = 'Formed'
    new_task_obj = Task(type_of_task, task_id, task_str, status, 'unknown')
    add_to_queue(new_task_obj, q)
    print(f'Object {new_task_obj} created with ID {new_task_obj.task_id}')
    conn.execute(f"INSERT INTO 'tasks' "
                 f"VALUES('"
                 f"{new_task_obj.task_type}', "
                 f"'{new_task_obj.task_id}', "
                 f"'{new_task_obj.task}', "
                 f"'{new_task_obj.status}', "
                 f"'{new_task_obj.result}')"
                 )
    conn.commit()
    return new_task_obj


# Функция формирования ID
def task_id_creator(type_of_task):
    if type_of_task == '-rev':
        tasks_id.append('RVRS' + str(len(tasks_id) + 1))
        print('The ID was successfully generated.')
    if type_of_task == '-ec':
        tasks_id.append('EVCV' + str(len(tasks_id) + 1))
        print('The ID was successfully generated.')
    return tasks_id[-1]


# Функция добавления в очередь
def add_to_queue(task_obj, q):
    q.put(task_obj)
    print(f'Object {task_obj} added to queue.')


# Функция проверки ID.
def id_validator(some_id):
    print(tasks_id)
    if some_id in tasks_id:
        return True
    else:
        return False

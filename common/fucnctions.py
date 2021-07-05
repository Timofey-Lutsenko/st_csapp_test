# coding=utf-8
from itertools import chain
import time


# Функция разворачивающая входные данные
def reverser(data):
    time.sleep(2)
    return data[::-1]


# Функция, замещающая нечетные буквы - четными
def data_converter(data):
    converted_data = list(
        chain(*(x for x in zip(
            data[1::2],
            data[::2]
        ))
              )
    )
    return converted_data


# Обработчик входных данных
def is_even_handler(user_data):
    if len(user_data) % 2 == 0:
        return ''.join(data_converter(user_data))
    else:
        alone_letter = user_data[-1]
        temp = data_converter(user_data[:-1])
        temp.append(alone_letter)
        time.sleep(5)
        return ''.join(temp)



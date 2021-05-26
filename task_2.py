"""
Задача 2
Дан файл, содержащий имена файлов, алгоритм хэширования (один из MD5/SHA1/SHA256) и соответствующие им хэш-суммы,
вычисленные по соответствующему алгоритму и указанные в файле через пробел. Напишите программу, читающую данный файл
и проверяющую целостность файлов.

Пример

Файл сумм:
file_01.bin md5 aaeab83fcc93cd3ab003fa8bfd8d8906
file_02.bin md5 6dc2d05c8374293fe20bc4c22c236e2e
file_03.bin md5 6dc2d05c8374293fe20bc4c22c236e2e
file_04.txt sha1 da39a3ee5e6b4b0d3255bfef95601890afd80709

Пример вызова:
<your program> <path to the input file> <path to the directory containing the files to check>

Формат вывода:
file_01.bin OK
file_02.bin FAIL
file_03.bin NOT FOUND
file_04.txt OK
"""

import hashlib
from secrets import compare_digest
from sys import argv


algorithms = {'md5': hashlib.md5(), 'sha1': hashlib.sha1(), 'sha256': hashlib.sha256()}
result = {True: 'OK', False: 'FAIL'}


def get_hash(filename, algorithm):
    """
    Функция рассчитывает хеш-сумму файла, используя
    переданный в аругментах алгоритм. Может работать
    с большими файлами, т.к. считывает файл блоками
    по 8192 байта (размер блоков можно изменить).
    """
    try:
        with open(f'{path_to_file}/{filename}', 'rb') as f:
            m = algorithms[algorithm]
            while True:
                data = f.read(8192)
                if not data:
                    break
                m.update(data)
            return m.hexdigest()
    except FileNotFoundError:
        return 'NOT FOUND'


def check_data(file_str):
    """
    Функция принимает строку файла с данными, разделяет
    её на имя, название алгоритма и хеш-сумму. Имя файла
    и название алгоритма отправляет в функцию расчета
    хеш-суммы и результат сравнивает с данными из строки.
    Возвращает результат сравнения.
    """
    file_name, algorithm, db_hash = file_str.split()
    check_hash = get_hash(file_name, algorithm)
    if check_hash == 'NOT FOUND':
        return file_name, check_hash
    check = compare_digest(db_hash, check_hash)
    return file_name, result[check]


if __name__ == "__main__":
    if len(argv) == 3:
        script_name, path_to_data, path_to_file = argv
        with open(path_to_data, 'r') as file:
            for line in file.readlines():
                name, res = check_data(line)
                print(f'{name} {res}')
    else:
        print('Неверно указаны аргументы для запуска скрипта. Попробуйте еще раз.')

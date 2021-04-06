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

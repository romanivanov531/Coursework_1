from functools import wraps


def logg(file_name=None):
    """Декоратор для записи результатов работы функции.
    Результатом должен быть датафрейм.
    Аргумент - название файла для записи в файл.
    Запись идет в директорию reports"""
    if file_name is None:
        file_name = 'report.txt'

    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            result = func(*args, **kwargs)
            with open(f'../reports/{file_name}', 'a', encoding='utf-8') as file:
                file.write(result.to_string(index=False))
            return result
        return inner
    return wrapper

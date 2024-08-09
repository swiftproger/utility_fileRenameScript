import os
import time

# Массив строк для удаления из имен файлов и каталогов
strings_to_remove = ["example1", "example2", "example3"]

# Массив строк для удаления файлов, если имя полностью совпадает
strings_to_delete = ["delete1", "delete2", "delete3"]

# Путь к директории, в которой будет производиться переименование
directory_path = "./"

# Счетчики переименованных и удаленных файлов и каталогов
renamed_files_count = 0
renamed_dirs_count = 0
deleted_files_count = 0


def remove_and_rename_in_directory(current_path):
    """Обход всех файлов и каталогов в указанной директории с целью переименования или удаления.

    Аргументы:
    current_path (str): Путь к директории, в которой проводится операция.
    """
    global renamed_files_count, renamed_dirs_count, deleted_files_count

    for root, dirs, files in os.walk(current_path, topdown=False):
        process_files(root, files)
        process_directories(root, dirs)


def process_files(root, files):
    """Обработка файлов: переименование или удаление в зависимости от соответствия строкам.

    Аргументы:
    root (str): Путь к текущей директории.
    files (list): Список файлов в текущей директории.
    """
    global renamed_files_count, deleted_files_count

    for file_name in files:
        if should_delete(file_name) or file_name.startswith("._"):
            delete_file(root, file_name)
        else:
            new_name = remove_strings_from_name(file_name)
            if new_name != file_name:
                rename_file(root, file_name, new_name)


def process_directories(root, dirs):
    """Обработка директорий: переименование или удаление в зависимости от соответствия строкам.

    Аргументы:
    root (str): Путь к текущей директории.
    dirs (list): Список директорий в текущей директории.
    """
    global renamed_dirs_count, deleted_files_count

    for dir_name in dirs:
        if should_delete(dir_name) or dir_name.startswith("._"):
            delete_directory(root, dir_name)
        else:
            new_name = remove_strings_from_name(dir_name)
            if new_name != dir_name:
                rename_directory(root, dir_name, new_name)


def should_delete(name):
    """Проверяет, нужно ли удалять файл или каталог, если имя полностью совпадает с одной из строк в массиве.

    Аргументы:
    name (str): Имя файла или каталога.

    Возвращает:
    bool: True, если файл или каталог должен быть удален, иначе False.
    """
    return name in strings_to_delete


def delete_file(root, file_name):
    """Удаляет файл и выводит сообщение об удалении.

    Аргументы:
    root (str): Путь к текущей директории.
    file_name (str): Имя удаляемого файла.
    """
    global deleted_files_count
    file_path = os.path.join(root, file_name)

    try:
        print(f"Удаление файла: {file_path}")
        os.remove(file_path)
        deleted_files_count += 1
    except FileNotFoundError:
        print(f"Ошибка: Файл не найден для удаления: {file_path}")
    except Exception as e:
        print(f"Ошибка при удалении файла {file_path}: {e}")


def delete_directory(root, dir_name):
    """Удаляет каталог и выводит сообщение об удалении.

    Аргументы:
    root (str): Путь к текущей директории.
    dir_name (str): Имя удаляемого каталога.
    """
    global deleted_files_count
    dir_path = os.path.join(root, dir_name)

    try:
        print(f"Удаление каталога: {dir_path}")
        os.rmdir(dir_path)
        deleted_files_count += 1
    except FileNotFoundError:
        print(f"Ошибка: Каталог не найден для удаления: {dir_path}")
    except OSError as e:
        print(f"Ошибка: Каталог не может быть удален (возможно, не пуст): {dir_path}. {e}")
    except Exception as e:
        print(f"Ошибка при удалении каталога {dir_path}: {e}")


def remove_strings_from_name(name):
    """Удаляет все вхождения строк из массива из имени файла или каталога.

    Аргументы:
    name (str): Имя файла или каталога.

    Возвращает:
    str: Измененное имя файла или каталога.
    """
    for check_string in strings_to_remove:
        name = name.replace(check_string, "")
    return name


def rename_file(root, old_name, new_name):
    """Переименовывает файл, если новое имя не существует, или добавляет суффикс для уникальности.

    Аргументы:
    root (str): Путь к текущей директории.
    old_name (str): Старое имя файла.
    new_name (str): Новое имя файла.
    """
    global renamed_files_count
    old_file_path = os.path.join(root, old_name)
    new_file_path = os.path.join(root, new_name)

    new_file_path = ensure_unique_name(new_file_path)

    try:
        os.rename(old_file_path, new_file_path)
        renamed_files_count += 1
        print(f"Файл переименован: {old_file_path} -> {new_file_path}")
    except FileNotFoundError:
        print(f"Ошибка: Файл не найден для переименования: {old_file_path}")
    except FileExistsError:
        print(f"Ошибка: Файл с именем {new_file_path} уже существует.")
    except Exception as e:
        print(f"Ошибка при переименовании файла {old_file_path} -> {new_file_path}: {e}")


def rename_directory(root, old_name, new_name):
    """Переименовывает каталог, если новое имя не существует, или добавляет суффикс для уникальности.

    Аргументы:
    root (str): Путь к текущей директории.
    old_name (str): Старое имя каталога.
    new_name (str): Новое имя каталога.
    """
    global renamed_dirs_count
    old_dir_path = os.path.join(root, old_name)
    new_dir_path = os.path.join(root, new_name)

    new_dir_path = ensure_unique_name(new_dir_path)

    try:
        os.rename(old_dir_path, new_dir_path)
        renamed_dirs_count += 1
        print(f"Каталог переименован: {old_dir_path} -> {new_dir_path}")
    except FileNotFoundError:
        print(f"Ошибка: Каталог не найден для переименования: {old_dir_path}")
    except FileExistsError:
        print(f"Ошибка: Каталог с именем {new_dir_path} уже существует.")
    except Exception as e:
        print(f"Ошибка при переименовании каталога {old_dir_path} -> {new_dir_path}: {e}")


def ensure_unique_name(path):
    """Генерирует уникальное имя, если файл или каталог с таким именем уже существует.

    Аргументы:
    path (str): Предлагаемое имя файла или каталога.

    Возвращает:
    str: Уникальное имя файла или каталога.
    """
    base, ext = os.path.splitext(path)
    counter = 1
    while os.path.exists(path):
        path = f"{base}_{counter}{ext}"
        counter += 1
    return path


def main():
    """Основная функция программы."""
    global start_time, end_time

    # Начало отсчета времени
    start_time = time.time()

    # Запуск функции переименования и удаления
    remove_and_rename_in_directory(directory_path)

    # Конец отсчета времени
    end_time = time.time()

    # Вывод итогов
    print(f"Переименовано файлов: {renamed_files_count}")
    print(f"Переименовано каталогов: {renamed_dirs_count}")
    print(f"Удалено файлов и каталогов: {deleted_files_count}")
    print(f"Время выполнения: {end_time - start_time:.2f} секунд")


if __name__ == '__main__':
    main()

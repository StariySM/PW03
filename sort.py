import os
import re
import shutil
import sys
import logging
from threading import Thread, Event, RLock, Semaphore
from time import sleep
from multiprocessing import Queue, Process, current_process
import concurrent.futures


logger = logging.getLogger()
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s: %(threadName)s - %(message)s')
stream_handler.setFormatter(formatter)


# папки для сортировки и перемещения в них соответствующих файлов
pathes = ["images", "video", "documents", "audio", "archives", "unknow"]


# создаем папки согласно списка pathes
def create_pathes(path0):
    for i in pathes:
        try:
            os.mkdir(path0 + "\\" + i)
        except FileExistsError:
            continue
            # print("папка", i, "уже существует")


# перечень обрабатываемых расширений
ext_dict = {
    'jpeg': pathes[0], 'png': pathes[0], 'jpg': pathes[0], 'svg': pathes[0],
    'avi': pathes[1], 'mp4': pathes[1], 'mov': pathes[1], 'mkv': pathes[1], '3gp': pathes[1],
    'doc': pathes[2], 'docx': pathes[2], 'txt': pathes[2], 'pdf': pathes[2], 'xlsx': pathes[2], 'pptx': pathes[2],
    'mp3': pathes[3], 'ogg': pathes[3], 'wav': pathes[3], 'amr': pathes[3],
    'zip': pathes[4], 'gz': pathes[4], 'tar': pathes[4], 'rar': pathes[4]
}


# создем словарь для транслитерации кириличного алфавита
cyr = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
translit = (
    "a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
    "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")
translit_dict = {}
for c, t in zip(cyr, translit):
    translit_dict[ord(c)] = t
    translit_dict[ord(c.upper())] = t.upper()


# функция для преобразования текста
def normalize(name: str):
    return re.sub(r'[^0-9|a-z|A-Z]', "_", name.translate(translit_dict))

# функция для удаления пустых папок
def remove_dir(path0):
    os.rmdir(path0)
    logging.debug(f'delete {path0}')

# функция для распаковки архивов
def unpack_arch():
    for p in os.listdir(path + "\\archives\\"):
        shutil.unpack_archive(path + "\\archives\\" + p, path + "\\archives\\" + p)
        os.remove(path0 + "\\" + p)
        logging.debug(f'unpack {path} "\\archives\\" {p}')

# функция для переноса файлов
def replace_files(q: Queue, path):
    nam = current_process().name
    logging.debug(f'{nam} start...')
    while not q.empty():
        path0 = q.get()
        name, ext = os.path.splitext(os.path.basename(path0))
        os.replace(path0, path + "\\" + ext_dict.get(ext[1:], "unknow") + "\\" + normalize(name) + ext)
        logging.debug(f'{nam} {os.path.basename(path0)} was replaced to {ext_dict.get(ext[1:])}')
    logging.debug(f'{nam} finish')
    sys.exit(0)

# функция добавления в очередь переноса файлов папки
def skan_path(root, name, q):
    nam = current_process().name
    logging.debug(f'{nam} add {os.path.join(root, name)} to Q')
    return q.put(os.path.join(root, name))


def main(path, n):
    create_pathes(path)
    q = Queue()
    for i in range(n):
        Process(target=replace_files, args=(q, path)).start()
    for root, dirs, files in os.walk(path):
        with concurrent.futures.ThreadPoolExecutor(n) as executor:
            list(executor.map(lambda x: skan_path(root, x, q), files))


if __name__ == "__main__":
    # path = "D:\\musor"
    # shutil.unpack_archive("D:\\musor.zip", "D:\\musor")
    path = str(sys.argv[1])
    n = int(sys.argv[2])
    main(path, n)

import pickle
from tkinter import *
from tkinter import messagebox as mbox
import os

def byte(w, path1):
    """
    Функци считывания базы из двоичного файла
    Автор:Матющенко А.А.
    :param w: Словарь словарей базы данных
    :param path1: Путь к двоичному файлу
    :return: Словарь словарей базы данных
    """
    f = open(path1, "rb")
    w = pickle.load(f)
    f.close()
    return w


def find_name(w,key,name):
    """
    Автор:Николайшвили Г.М.
    Функция поиска записей с именем, введённым пользователем
    Получает на вход список словарей w,ключ для определения поиска key, и имя поля по которому ведется поиск naame
    Возвращает список ключей списка w
    """
    f = []
    if key=="цвет(а)":
        for i in w.keys():
            a=w[i][key]
            l=a.split(",")
            if name in l:
                f.append(w[str(i)])
        return f
    else:
        for i in w.keys():
            if w[i][key] == name:
                f.append(w[str(i)])
        return f



def save(w, path3):
    """
    Автор:Туракулов А.У.
    Функция сохранения словаря словарей в файл
    Получает на вход словарь словарей
    """
    f = open(path3, "wb")
    pickle.dump(w, f)
    f.close()


def change_node(w, key,cmodelname,ccomplect,cfirm,csex,cprice,ccolor,ccountry,cnumber):
    """
    Автор:Матющенко А.А.
    Функция изменения записи в словаре w с ключом key
    :param w: Словарь словарей, содержащий базу данных
    :param key: Ключ, определяющий какую запись изменять
    :param cmodel,ccomplect,cfirm,csex,cprice,ccolor,ccountry,cnumber:новые значения полей записи бд
    :return: Возвращает словарь словарей с изменённой записью
    """
    try:
        w[str(key)]["название модели"] = cmodelname
        w[str(key)]["комплектация"] = ccomplect
        w[str(key)]["фирма"] = cfirm
        w[str(key)]["пол"] = csex
        w[str(key)]["стоимость"] = cprice
        w[str(key)]["цвет(а)"] = ccolor
        w[str(key)]["страна производитель"]= ccountry
        w[str(key)]["количество"]= cnumber
    except KeyError:
        mbox.showerror("Отсутсвует выделение", "Не выбрана строка для редактирования. Выберите и попробуйте снова")
    return w


def delete_node(w, key):
    """
    Автор: Николайшвили Г.М.
    Функция изменения записи в словаре w с ключом key
    :param w: Словарь словарей, содержащий базу данных
    :param key: Ключ, определяющий какую запись удалить
    :return: Возвращает изменённый словарь словарей
    """
    try:
        w.pop(str(key))
    except KeyError:
        mbox.showerror("Отсутсвует выделение", "Не выбрана строка для удаления. Выберите и попробуйте снова")
    return w


def add_node(w,nmodelname,ncomplect,nfirm,nsex,nprice,ncolor,ncountry,nnumber):
    """
    Автор: Туракулов А.У.
    :param :nmodelname,ncomplect,nfirm,nsex,nprice,ncolor,ncountry,number:значения добавляемой в бд записи
    :param w: Словарь словарей, содержащий базу данных
    :return: Возвращает изменённый словарь словарей
    """
    i = 0
    while str(i)  in w.keys():
        i+=1
    w[str(i)] = {
    "название модели" : nmodelname,
    "комплектация" : ncomplect,
    "фирма" : nfirm,
    "пол" : nsex,
    "стоимость" : nprice,
    "цвет(а)" : ncolor,
    "страна производитель" : ncountry,
    "количество" : nnumber
    }
    return w


def find_mensh(w, key, num):
    """
    Автор: Матющенко А.А.
    Функция поиска записей, значение в поле key которых меньше num
    :param w: Словарь словарей с данными базы
    :param num: Значение столбца
    :param key: Ключ столбца, в котором происходит поиск
    :return: Список подходящих записей
    """
    f = []
    try:
        for a in w.keys():
            if int(w[a][key]) <= num:
                f.append(w[a])
    except KeyError:
        print("Нет такого ключа")
    finally:
        return f


def find_bolsh(w, key, num):
    """
    Автор: Николайшвили Г.М.
    Функция поиска записей, значение в поле key которых больше num
    :param w: Словарь словарей с данными базы
    :param num: Значение столбца
    :param key: Ключ столбца, в котором происходит поиск
    :return: Список подходящих записей
    """
    f = []
    try:
        for a in w.keys():
            if int(w[a][key]) >= num:
                f.append(w[a])
    except KeyError:
        print("Нет такого ключа")
    finally:
        return f


def find_between(w, key, min, max):
    """
    Автор: Туракулов А.У.
    Функция поиска записей, значение в поле key которых больше min и меньше max
    :param w: Словарь словарей с данными базы
    :param min: минимальное значение столбца
    :param max: максимальное значение столбца
    :param key: Ключ столбца, в котором происходит поиск
    :return: Список подходящих записей
    """
    f = []
    try:
        for a in w.keys():
            if (int(w[a][key]) >= min )& (int(w[a][key]) <= max):
                f.append(w[a])
    except KeyError:
        print("Нет такого ключа")
    return f

def summary(f, askentry, askwindow):
    """
    Автор: Матющенко А.А.
    Функция подведения итогов: подсчёт записей, вычисления среднего значения, разброса, запись в текстовый файл
    :param f: Список словарей, выбранных другой функцией
    :param outname: Имя выходного файла
    Функция ничего не возвращает
    """
    outname = askentry.get()
    if outname == '':
        mbox.showerror("Отсутствует название", "Введите название файла")
        return
    keys = ["стоимость","количество"]
    average = {}  # Словарь, содержащий средние значения клюей keys, его нужно вывести в файл вместе с записями
    kvadr = {}  # Словарь КВАДРАТОВ среднекважратичных отклонений от среднеарифметического, вывод в файл
    disp = {}  # Словарь дисперсии, вывод в файл
    k = len(f)
    if k == 0:
        for key in keys:
            average[key] = 0
            kvadr[key] = 0
            disp[key] = 0
    elif k == 1:
        for key in keys:
            s = 0
            kv = 0
            for node in f:
                s += float(node[key])
                kv += float(node[key])*float(node[key])
            average[key] = float(s)/k
            kvadr[key] = 0
            disp[key] = 0
    else:
        for key in keys:
            s = 0
            kv = 0
            for node in f:
                s += float(node[key])
                kv += float(node[key])*float(node[key])
            average[key] = float(s)/k
            kvadr[key] = kv/k - average[key]*average[key]
            disp[key] = (kv - 2*average[key]*s + k*average[key]*average[key])/(k-1)
    outname += '.txt'
    path = os.getcwd()
    n = path.find("\Scripts")
    path1 = os.path.join(path[0:n] + "\Output", outname)
    fileout = open(path1, "w")
    for node in f:
        print(node['название модели'], node['комплектация'], node['фирма'], node['пол'], node['стоимость'], node['цвет(а)'],node["страна производитель"], node['количество'], file=fileout)
    print("Средние значения", file=fileout)
    print("Стоимость: ", average['стоимость'], "Отклонение от среднего арифметического: ", kvadr['стоимость']**0.5,
          "Дисперсия: ", disp['стоимость'], file=fileout)
    print("Количество: ", average['количество'], "Отклонение от среднего арифметического: ", kvadr['количество']**0.5,
          "Дисперсия: ", disp['количество'], file=fileout)
    mbox.showinfo("Сохранено!", "Сохранение успешно")
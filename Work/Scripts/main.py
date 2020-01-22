from tkinter import *
import pickle
import os
from tkinter import messagebox as mbox
import sys

path = os.getcwd()
n = path.find("\Scripts")
path1 = os.path.join(path[0:n] + "\Data", "Сross.pic")  # ОП  до бд чтобы прога работала везде куда ее скачают
path2 = os.path.join(path[0:n] + "\Graphics","fon.png")  # ОП  до картинки фона чтобы прога работала везде куда ее скачают
path3 = os.path.join(path[0:n] + "\Data", "Сross(updated).pic")  # ОП  до бд  вывода чтобы прога работала везде куда ее скачают
path4 = os.path.join(path[0:n] + "\Library") #путь до билиотеки стандартных функций
path8 = os.path.join(path[0:n] + "\Scripts", "colors.txt") #путь до текстового документа с цветовым оформлением
w={}
sys.path.append(path4)
from ourmodule import* #ПОДКЛЮЧЕНИЕ БИБИОТЕКИ СТАНДАРТНЫХ ФУНКЦИЙ БАЗЫ ДАННЫХ

def colors(path8, length):
    """
    Функция считывания параметров интерфейса из файла
    Автор: Туракулов А.У
    :param path8: Путь к текстовому файлу с параметрами
    :param length: Количество цветов
    :return: Список, состоящий из количества length цветов, названия шрифта и размера шрифта
    """
    a = []
    for i in range(length):
        a.append("white")
    f = open(path8, "r")
    i = 0
    for k in f:
        k = k.rstrip('\n')
        try:
            a[i] = str(k)
        except IndexError:
            a.append(str(k))
        i += 1
    f.close()
    return a

a = []
a = colors(path8, 4)
butcolor = a[0]
bgcolor1 = a[1]
bgcolor2 = a[2]
bgcolor3 = a[3]
mainfont = (str(a[4]), int(a[5]))


def open_w_summary(f):
    """
    Открывает диалогове окно для подведения  стат итогов по выборке
    Автор: Туракулов А.У
    :param f: Список словарей, выбранных другой функцией
    Функция ничего не возвращает
    """   
    askwindow = Tk()
    askwindow.title("Сохранение файла")
    asklabel = Label(askwindow, text = "Введите название файла")
    asklabel.grid(row=0)
    askentry = Entry(askwindow)
    askentry.grid(row=1)
    askentry.insert(0, "result_saved")
    askbutton = Button(askwindow, text="Сохранить файл")
    askbutton.bind("<Button-1>", lambda e: summary(f, askentry, askwindow))
    askbutton.grid(row=2)

def onInfo():
    """
    Функция выводит сообщение с подсказкой
    Автор: Туракулов А.У.
    Функция ничего не возвращает
    """
    mbox.showinfo("Подсказка при редактировании", "Чтобы удалить запись выберете ее в списке,затем нажмите кнопку <Удалить выбранную запись>\nЧтобы отредактировать запись выберете запись которую необходимо отредактировать из списка,введите новые значения записи в поля,и затем нажмите кнопку <Редактировать запись>\nЧтобы добавить запись, введите в поля данные новой записи и нажмите кнопку <Добавить запись>\n")

def update_listbox(listbox, params=None):
    """
    Функция обновляет листбокс
    Автор: Туракулов А.У
    """
    listbox.delete(0,END)
    if not params:
        params = w.keys()
    for i in params:
        listbox.insert(END,str(i)+" "+str(w[str(i)]['название модели']) + '. \"' + str(w[str(i)]['комплектация']) + '-\"' + str(w[str(i)]['фирма']) + '-' + str(w[str(i)]["пол"]) +"/"+ str(w[str(i)]["стоимость"]) + ' '+(w[i]["цвет(а)"])+'-'+(w[i]['страна производитель'])+'-'+str(w[str(i)]['количество']))

def load_base_button():
    """
    Функция загружает базу
    Автор: Туракулов А.У
    Возвращает словарь словарей базы данных
    """
    global w
    w = byte(w, path1)
    return w

def open_w_findbetween():
    """
    Открывает диалогове окно для нахождения записи в диапазоне
    Автор: Туракулов А.У
    Функция ничего не возвращает
    """
    betweenwind = Tk()
    #betweenwind.geometry("940x480")
    betweenwind.title("Найти записи от и до опредленного значения")
    message = Label(betweenwind, text="Выберете интересующий ключ и диапазон")
    message.grid(row=1, column=3, sticky=NSEW)
    edit1 = Entry(betweenwind, text="От", width=20)
    edit1.insert(0,"ОТ")
    edit1.grid(row=3, column=3, sticky=NSEW)
    edit2 = Entry(betweenwind, text="До", width=20)
    edit2.insert(0,"ДО")
    edit2.grid(row=4, column=3, sticky=NSEW)
    kluchi = [ "стоимость","количество" ]
    kluch = StringVar()
    kluch.set(kluchi[0])
    opt = OptionMenu(betweenwind, kluch, *kluchi)
    opt.grid(row=5, column=3, sticky=NSEW)

    def start():
        """
        Функция получает вводимые значения с клавиатуры,затем после проверки запускает функцию 
        подведения итогов (средние значения) и отображает их на экране
        После этого можно сохранить в текстовый файл
        При неккоректно введенных данных появляется сообщение с предупреждением
        Автор: Туракулов А.У.
        Функция ничего не возвращает
        """
        if edit1.get()=='':
            mbox.showerror("Пустые поля", "Заполните поле положительными числами")
            return
        try:
            int(edit1.get())
        except ValueError:
            mbox.showerror("Неверный тип данных", "Заполните поле положительными числами")
            return
        if edit2.get()=='':
            mbox.showerror("Пустые поля", "Заполните поле положительными числами")
            return
        try:
            int(edit2.get())
        except ValueError:
            mbox.showerror("Неверный тип данных", "Заполните поле положительными числами")
            return
        start_function.grid_remove()
        opt.grid_remove()
        edit1.grid_remove()
        edit2.grid_remove()
        message.grid_remove()    
        num1 = int(edit1.get())
        num2 = int(edit2.get())
        key = kluch.get()
        f = find_between(w, key, num1, num2)
        itogo = Button(betweenwind, text="Подвести итоги")
        itogo.bind("<Button-1>",lambda k:open_w_summary(f))
        itogo.grid(row=31, column=4, sticky=NSEW)
        k=0
        for i in f:
            j=0
            for l in i.keys():
                l = Label(betweenwind, text=i[l], relief=RIDGE)
                l.grid(row=k, column=j, sticky=NSEW)
                j += 1
            k+=1
    start_function = Button(betweenwind, text="Старт", command=start)
    start_function.grid(row=6, column=3, sticky=NSEW)
    betweenwind.mainloop()
    
def open_w_findbolsh():
    """
    Функция для вызова диалогового окна для нахождения записи больше указанного поля ключа
    Автор: Туракулов А.У
    Функция ничего не возвращает
    """
    bolshwind = Tk()
    #bolshwind.geometry("940x480")
    bolshwind.title("Найти записи больше определенного значения")
    message = Label(bolshwind, text="Выберете интересующий ключ и введите значение")
    message.grid(row=1, column=3, sticky=NSEW)
    edit = Entry(bolshwind, width=20)
    edit.grid(row=3, column=3, sticky=NSEW)
    kluchi = [ "стоимость", "количество"]
    kluch = StringVar()
    kluch.set(kluchi[0])
    opt = OptionMenu(bolshwind, kluch, *kluchi)
    opt.grid(row=4, column=3, sticky=NSEW)

    def start():
        """
        Функция получает вводимые значения с клавиатуры,затем после проверки запускает функцию 
        подведения итогов (средние значения) и отображает их на экране
        После этого можно сохранить в текстовый файл
        При неккоректно введенных данных появляется сообщение с предупреждением
        Автор: Туракулов А.У
        Функция ничего не возвращает
        """
        if edit.get()=='':
            mbox.showerror("Пустые поля", "Заполните поле положительными числами")
            return
        try:
            int(edit.get())
        except ValueError:
            mbox.showerror("Неверный тип данных", "Заполните поле положительными числами")
            return
        start_function.grid_remove()
        opt.grid_remove()
        edit.grid_remove()
        message.grid_remove()
        num = int(edit.get())
        key = kluch.get()
        f = find_bolsh(w, key, num)
        itogo = Button(bolshwind,text="Подвести итоги")
        itogo.bind("<Button-1>", lambda k: open_w_summary(f))
        itogo.grid(row=31,column=4,sticky=NSEW)
        k=0
        for i in f:
            j=0
            for l in i.keys():
                l = Label(bolshwind, text=i[l], relief=RIDGE)
                l.grid(row=k, column=j, sticky=NSEW)
                j += 1
            k+=1

    start_function = Button(bolshwind, text="Старт", command=start)
    start_function.grid(row=5, column=3, sticky=NSEW)
    bolshwind.mainloop()

def open_w_findmensh():
    """
    Функция для вызова диалогового окна для нахождения записи меньше указанного поля ключа
    Автор: Туракулов А.У.
    Функция ничего не возвращает
    """
    menshwind = Tk()
    #menshwind.geometry("940x480")
    menshwind.title("Найти записи меньше определенного значения")
    message = Label(menshwind, text="Выберете интересующий ключ и введите значение")
    message.grid(row=1, column=3, sticky=NSEW)
    edit = Entry(menshwind, width=20)
    edit.grid(row=3, column=3, sticky=NSEW)
    kluchi = [ "стоимость","количество"]
    kluch = StringVar()
    kluch.set(kluchi[0])
    opt = OptionMenu(menshwind, kluch, *kluchi)
    opt.grid(row=4, column=3, sticky=NSEW)
    def start():
        """
        Функция получает вводимые значения с клавиатуры, затем после проверки запускает функцию 
        подведения итогов (средние значения) и отображает их на экране
        После этого можно сохранить в текстовый файл
        При неккоректно введенных данных появляется сообщение с предупреждением
        Автор: Матющенко А.А.
        Функция ничего не возвращает
        """ 
        if edit.get()=='':
            mbox.showerror("Пустые поля", "Заполните поле положительными числами")
            return
        try:
            int(edit.get())
        except ValueError:
            mbox.showerror("Неверный тип данных", "Заполните поле положительными числами")
            return
        start_function.grid_remove()
        opt.grid_remove()
        edit.grid_remove()
        message.grid_remove()
        num = int(edit.get())
        key = kluch.get()      
        f = find_mensh(w, key, num)  
        itogo = Button(menshwind, text="Подвести итоги")
        itogo.bind("<Button-1>", lambda k: open_w_summary(f))
        itogo.grid(row=31, column=4, sticky=NSEW)
        k=0
        for i in f:
            j=0
            for l in i.keys():
                l = Label(menshwind, text=i[l], relief=RIDGE)
                l.grid(row=k, column=j, sticky=NSEW)
                j += 1
            k+=1
    start_function = Button(menshwind, text="Старт", command=start)
    start_function.grid(row=5,column=3,sticky=NSEW)
    menshwind.mainloop()
    
def open_w_findname():
    """
    Функция для вызова диалогового окна для нахождения записи по строковому значению
    Автор: Туракулов А.У
    Функция ничего не возвращает
    """
    findname= Tk()
    #findname.geometry("940x480")
    findname.title("Найти записи c именем")
    message = Label(findname, text="Выберете текстовое поле для поиска и введите значение")
    message.grid(row=1, column=3, sticky=NSEW)
    edit = Entry(findname, width=20)
    edit.grid(row=3, column=3, sticky=NSEW)
    kluchi = ["комплектация","фирма","пол", "цвет(а)", "страна производитель"]
    kluch = StringVar()
    kluch.set(kluchi[0])
    opt = OptionMenu(findname, kluch, *kluchi)
    opt.grid(row=4, column=3, sticky=NSEW)
    def start():
        """
        Функция получает вводимые значения с клавиатуры,затем после проверки запускает функцию 
        подведения итогов (средние значения) и отображает их на экране
        После этого можно сохранить в текстовый файл
        При неккоректно введенных данных появляется сообщение с предупреждением
        Автор: Туракулов А.У.
        Функция ничего не возвращает
        """
        if edit.get()=='':
            mbox.showerror("Пустое поле", "Для поиска заполните поле русскими буквами")
            return
        start_function.grid_remove()
        edit.grid_remove()
        message.grid_remove()
        opt.grid_remove() 
        name = edit.get()
        key = kluch.get()
        f = find_name(w,key,name)
        itogo = Button(findname, text="Подвести итоги")
        itogo.bind("<Button-1>", lambda k: open_w_summary(f))
        itogo.grid(row=31, column=4, sticky=NSEW)
        k=0
        for i in f:
            j=0
            for l in i.keys():
                l = Label(findname, text=i[l], relief=RIDGE)
                l.grid(row=k, column=j, sticky=NSEW)
                j += 1
            k+=1
    start_function = Button(findname, text="Старт", command=start)
    start_function.grid(row=5,column=3,sticky=NSEW)
    findname.mainloop()
    
def open_w_redbd():
    """
    Функция для вызова диалогового окна для просмотра, редактирования и добавления записей базы данных
    Автор: Туракулов А.У
    Функция ничего не возвращает
    """
    redbd=Tk()
    onInfo()
    redbd.geometry("840x545")
    redbd.resizable(width=False, height=False)
    redbd.title("Просмотр и редактирование базы")
    scroll = Scrollbar(redbd)
    list=Listbox(redbd, yscrollcommand=scroll.set, height=20, width=140, selectmode=SINGLE)
    def delete():
        """
        Функция удаляет запись в базе данных
        Функция не имеет параметров
        Автор: Туракулов А.У
        Функция ничего не возвращает
        """
        selection = list.curselection()
        a=list.get(selection[0])
        l=a.split()
        a=l[0]
        list.delete(selection[0])
        a=int(a)
        delete_node(w,a)
        
    def add():
        """
        Функция добавляет запись в базе данных
        При неправильно введенных данных, появляется сообщение о том что данные неправильные или пустые поля
        Функция не имеет параметров
        Автор: Туракулов А.У
        Функция ничего не возвращает
        """
        new_modelname = modelnameentry.get()
        new_complect = complectentry.get()
        new_firm = firmentry.get()
        new_sex = sexentry.get()
        new_price = priceentry.get()
        new_color = colorentry.get()
        new_country = countryentry.get()
        new_number = numentry.get()
        if new_modelname == '' or new_complect == '' or new_firm == "" or new_sex == "" or new_price == "" or new_color =='' or new_country==''or new_number=='':
            mbox.showerror("Пустые поля", "Заполните поля перед редактированием записи")
            return
        try:
            int(new_price)
            int(new_number)
        except ValueError:
            mbox.showerror("Неправильный тип данных", "Заполните поля верным типом данных")
            return
        add_node(w,new_modelname,new_complect,new_firm,new_sex,new_price,new_color,new_country,new_number)
        update_listbox(list)
        
    def change():
        """
        Функция редактирует запись в базе данных
        При неправильно введенных данных, появляется сообщение о том что данные неправильные или пустые поля
        Функция не имеет параметров
        Автор: Туракулов А.У
        Функция ничего не возвращает
        """
        selectionc = list.curselection()
        a = list.get(selectionc[0])
        l = a.split()
        a = l[0]
        a = int(a)
        new_modelname = modelnameentry.get()
        new_complect = complectentry.get()
        new_firm = firmentry.get()
        new_sex = sexentry.get()
        new_price = priceentry.get()
        new_color = colorentry.get()
        new_country = countryentry.get()
        new_number = numentry.get()
        if new_modelname == '' or new_complect == '' or new_firm == "" or new_sex == "" or new_price == "" or new_color =='' or new_country==''or new_number=='':
            mbox.showerror("Пустые поля", "Заполните поля перед редактированием записи")
            return
        try:
            int(new_price)
            int(new_number)
        except ValueError:           
            mbox.showerror("Неправильный тип данных", "Заполните поля верным типом данных")
            return
        list.delete(selectionc[0])
        change_node(w,a, new_modelname, new_complect, new_firm, new_sex, new_price, new_color, new_country, new_number)
        update_listbox(list)
    update_listbox(list)
    scroll.config(command=list.yview)
    list.grid(row=2, column=1, columnspan=10, sticky=NSEW)
    
    modelnamelabel = Label(redbd,text="Название модели")
    modelnamelabel.grid(row=4, column=1,sticky=NSEW)
    modelnameentry = Entry(redbd, width=30)
    modelnameentry.grid(row=4, column=2, sticky=NSEW)
    
    complectlabel = Label(redbd,text="Тип обуви")
    complectlabel.grid(row=5, column=1,sticky=NSEW)
    complectentry = Entry(redbd, width=30)
    complectentry.grid(row=5,column=2, sticky=NSEW)
    
    firmlabel = Label(redbd,text="Фирма-изготовитель")
    firmlabel.grid(row=7, column=1,sticky=NSEW)
    firmentry = Entry(redbd,width=30)
    firmentry.grid(row=7, column=2, sticky=NSEW)
    
    sexlabel = Label(redbd,text="Пол")
    sexlabel.grid(row=8, column=1,sticky=NSEW)
    sexentry = Entry(redbd,width=30)
    sexentry.grid(row=8, column=2, sticky=NSEW)
    
    pricelabel = Label(redbd,text="Стоимость")
    pricelabel.grid(row=9, column=1,sticky=NSEW)
    priceentry = Entry(redbd,width=30)
    priceentry.grid(row=9,column=2,sticky=NSEW)
    
    colorlabel = Label(redbd,text="Цвет")
    colorlabel.grid(row=10, column=1,sticky=NSEW)
    colorentry = Entry(redbd,width=30)
    colorentry.grid(row=10,column=2,sticky=NSEW)
    
    countrylabel = Label(redbd,text="Страна производства")
    countrylabel.grid(row=11, column=1,sticky=NSEW)
    countryentry = Entry(redbd, width=30)
    countryentry.grid(row=11, column=2, sticky=NSEW)
    
    numlabel = Label(redbd,text="Количество")
    numlabel.grid(row=12, column=1,sticky=NSEW)
    numentry = Entry(redbd, width=30)
    numentry.grid(row=12, column=2, sticky=NSEW)
    
    del_button = Button(redbd, text="Удалить выбранную запись", command=delete)
    del_button.grid(row=1, column=3, sticky=NSEW)
    
    Change_button= Button(redbd,text="Редактировать запись",command=change)
    Change_button.grid(row=17,column=2,sticky=NSEW)
    
    plus_button=Button(redbd, text="Добавить запись",command=add)
    plus_button.grid(row=1,column=2, sticky=NSEW)
    
    Save_button=Button(redbd, text="Сохранить изменения")
    Save_button.bind("<Button-1>",lambda e:save(w,path3))
    Save_button.grid(row=1,column=4,sticky=NSEW)
    
    scroll.grid(row=2, column=15, sticky=NSEW) 
    update_listbox(list)
    scroll.config(command=list.yview)
    list.grid(row=2, column=1, columnspan=10, sticky=NSEW)
    scroll.grid(row=2, column=13, sticky=NSEW)
    
    redbd.mainloop()

def mainInfo():
    """
    Функция выводит сообщение с подсказкой
    Автор: Туракулов А.У
    """
    mbox.showinfo("Подсказка", "Для начала использования нужно загрузить базу данных\nнажав на кнопку <Загрузить базу данных>, затем нажать на кнопку <Обновить таблицу>")


Root = Tk()
Root.geometry("845x505")
Root.resizable(width=False,height=False)
Root.title("База данных магазина спортивной обуви")
C = Canvas(Root, bg="blue", height=250, width=300)
filename = PhotoImage(file=path2)
background_label = Label(Root, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
top_frame = Frame(Root)
top_frame.grid(row=1, column=0)
bottom_frame = Frame(Root)
bottom_frame.grid(row=2,column=0)
scroll = Scrollbar(bottom_frame)
list=Listbox(bottom_frame, yscrollcommand=scroll.set, height=20, width=140, selectmode=SINGLE)
scroll.config(command=list.yview)
list.grid(row=2, column=0, columnspan=13, sticky=NSEW)
update_listbox(list)
Fresh=Button(Root,text="Обновить таблицу",height=3,command = lambda :update_listbox(list), bg=butcolor, font=mainfont)
LoadBaseBut = Button(top_frame, text="Загрузить базу данных",height=3,command =lambda :load_base_button(),bg=butcolor, font=mainfont)
LoadBaseBut.grid(row=2,column=1,sticky=NSEW)
MenshButton = Button(top_frame, text="Найти меньше",height=3, command=open_w_findmensh,bg=butcolor, font=mainfont)
MenshButton.grid(row=1, column=1,sticky=NSEW)
BolshButton = Button(top_frame,text= "Найти больше ",height=3,command=open_w_findbolsh,bg=butcolor, font=mainfont)
BolshButton.grid(row=1, column=2,sticky=NSEW)
BolshButton = Button(top_frame,text= "Найти в диапазоне",height=3,command=open_w_findbetween,bg=butcolor, font=mainfont)
BolshButton.grid(row=1, column=3,sticky=NSEW)
NameButton = Button (top_frame,text="Поиск по имени",height=3, command=open_w_findname,bg=butcolor, font=mainfont)
NameButton.grid(row=2,column=3,sticky=NSEW)
BDButton= Button(top_frame, text="Просмотр и редактирование базы данных",height=3,command=open_w_redbd ,bg=butcolor, font=mainfont)
BDButton.grid(row=2, column= 2,sticky=NSEW)
Fresh.grid(row=20,column=0)
C.grid()
mainInfo()
Root.mainloop()

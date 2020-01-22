import pickle as pic
f = open("Base.txt", "r")
n = 0
w = {}
keys = ["название модели","комплектация","фирма","пол", "стоимость", "цвет(а)", "страна производитель","количество"]
for string in f:
    string = string.rstrip()
    a = string.split()
    print(a)
    w[str(n)] = {'название модели':a[0], 'комплектация':a[1], 'фирма':a[2], 'пол':a[3], 'стоимость':a[4], 'цвет(а)':a[5], 'страна производитель':a[6],'количество':a[7]}
    n += 1
k = open("Сross.pic", "wb")
pic.dump(w, k)
f.close()
k.close()

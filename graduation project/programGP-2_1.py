from tkinter import *
from tkinter import ttk
import numpy as np 
import sys
import glob
import serial 
import time
import math

root = Tk()
root.title("ВАХ с ХП-2")
#root.iconbitmap(r'icon.ico')
root.geometry("1320x680")
root.resizable(width=False, height=False)



# лейблы
label_tx = Label(root, text = "Выбор порта: ", font="Arial 14" )   
label_tx.place(x = 5, y = 5)

label_tx = Label(root, text = "Выбор осей: ", font="Arial 14" )   
label_tx.place(x = 5, y = 100)

label_tx = Label(root, text = "Ось X: ", font="Arial 12" )   
label_tx.place(x = 5, y = 130)

label_tx = Label(root, text = "Ось Y: ", font="Arial 12" )   
label_tx.place(x = 5, y = 180)

label_tx = Label(root, text = "Усреднение: ", font="Arial 14" )   
label_tx.place(x = 5, y = 270)

label_tx = Label(root, text = "(количество точек для усреднения)", font="Arial 8" )   
label_tx.place(x = 10, y = 295)

label_tx = Label(root, text = "Задержка:", font="Arial 14" )   
label_tx.place(x = 5, y = 380)

label_tx = Label(root, text = "Перед снятием:", font="Arial 12" )   
label_tx.place(x = 5, y = 410)

label_tx = Label(root, text = "Между точками для уср.:", font="Arial 12" )   
label_tx.place(x = 5, y = 460)

label_copyright = Label(root, text = "©Сделано Ильёй в 2021", font="Arial 8")  
label_copyright.place(x = 5, y = 655)


# Поле графика
canvas = Canvas(root, width=1090, height=680, bg="white")
canvas.pack(side = "right")



frame = Frame(root)
frame.pack(pady = 35)

# Линии сетки по вертикали
for y in range(21):
    k = 50 * y
    canvas.create_line(45+k, 645, 45+k, 45, width=1, fill="lightgrey")

# Линии сетки по горизотали 

for x in range(13):
    k = 50 * x
    canvas.create_line(45, 45+k, 1045, 45+k, width=1, fill="lightgrey")

# ось Y
canvas.create_line(545, 35, 545, 645, width=1, arrow=FIRST, fill="black")

# ocь X
canvas.create_line(45, 345, 1055, 345, width=1, arrow=LAST, fill="black")

# что по осям X и Y
canvas.create_text(565, 30, text = "I, мкА", fill="black")
canvas.create_text(1070, 341, text = "U, В", fill="black")

# сканирование портов 
result = []
if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
for port in ports: 
    try:
        s = serial.Serial(port)
        s.close()
        result.append(port)
    except (OSError, serial.SerialException):
            pass


# комбобокс с портами
menuport = ttk.Combobox(root)
menuport['values'] = result
menuport.place(x = 20, y = 40)

# вызов функции serial и выбор частоты на которой мы будем работать с ардуино
ser = serial.Serial()
ser.baudrate = 9600

# функция выбора порта
def portopen():
    ser.port = menuport.get()
    print(ser.port)  
    ser.open()

# комбобоксы с размерами осей
coords_y = [500, 50, 5, 0.5]
coords_x = [1, 2.5, 5]
menu_coordsX = ttk.Combobox(root, values = coords_x)
menu_coordsX.place(x = 20, y = 155)
menu_coordsY = ttk.Combobox(root, values = coords_y)
menu_coordsY.place(x = 20, y = 205)
# комбобокс с количеством точек для усреднения
usredn = [1, 5, 10, 15, 20, 40]
menu_usredn = ttk.Combobox(root, values = usredn)
menu_usredn.place(x = 20, y = 320)
# комбобоксы с задержками перед снятием и между точками для усреднения
delay_1 = [50, 100, 150, 200]
delay_2 = [10, 15, 20, 30]
menu_delay_1 = ttk.Combobox(root, values = delay_1)
menu_delay_1.place(x = 20, y = 435)
menu_delay_2 = ttk.Combobox(root, values = delay_2)
menu_delay_2.place(x = 20, y = 485)


#функция вывода значений полученых с ардуино на график
def vivod():
    global VAH 
    linVAH_out = []
    z = []
    ser.write(b'1')                  # сигнал который мы посылаем на ардуино(после него начнется сканирование)
    
    def koef1(s_1):
        if s_1 == '5':
            z_1 = 100
        elif s_1 == '2.5':
            z_1 = 50/0.25
        elif s_1 == '1':
            z_1 = 50/0.1
        return z_1

    def koef2(s_2):
        if s_2 == '500':
            z_2 = 50/83.33
        elif s_2 == '50':
            z_2 = 50/8.333
        elif s_2 == '5':
            z_2 = 50/0.8333
        elif s_2 == '0.5':
            z_2 = 50/0.0833
        return z_2

    for w in range(412):
            data = ser.readline()        # 
            if len(data) >= 1:           # проверка на наличие данных с ардуино1 
                z.append(data)
    o = np.array(z, float)
    o1 = o.reshape(103, 4)
    I = 345 - (o1[:,0] - o1[:,1])*koef2(menu_coordsY.get())
    U = (o1[:,2] - o1[:,3])*koef1(menu_coordsX.get())  + 545
    linVAH_I = I.tolist()  
    linVAH_V = U.tolist()
    while linVAH_V or linVAH_I:                     # цикл объединения списков тока и напряженя в один для дальнейшего вывода 
        try:
            linVAH_out.append(linVAH_V.pop(0))      
        except: pass
        try:
            linVAH_out.append(linVAH_I.pop(0))
        except: pass
    print(o1)
    VAH = canvas.create_line(linVAH_out, fill="red", tag="line1") 

# выбор порта
btn_port = Button(root, text="Выбрать порт", command = portopen)
btn_port.place(x = 20, y = 70)

# очистка поля
def ochist():
    canvas.delete('line1')
# функция выставления значений под осями
def osy():
    canvas.delete('OS_Y')
    canvas.delete('OS_X')

    k = 0
    s = 0

    Znach_X = menu_coordsX.get()
    Znach_Y = menu_coordsY.get()
    print(Znach_X + " " + Znach_Y)

    if Znach_X == '1':
        ser.write(b'4')
    elif Znach_X == '2.5':
        ser.write(b'3')
    elif Znach_X == '5':
        ser.write(b'2')

    if Znach_Y == '500':
        ser.write(b'5')
    elif Znach_Y == '50':
        ser.write(b'6')
    elif Znach_Y == '5':
        ser.write(b'7')
    elif Znach_Y == '0.5':
        ser.write(b'8')

    OS_X = np.linspace(-float(Znach_X), float(Znach_X), 21)
    OS_Y = np.linspace(float(Znach_Y), -float(Znach_Y), 13)

     # значения по Y
    for i in OS_Y:
        canvas.create_text(528, 38+k, text = round(i, 2), fill="black", tag = 'OS_Y')
        k += 50 
    
    # Значения по X
    for t in OS_X:
        canvas.create_text(55+s, 352, text = round(t, 2), fill="black", tag = 'OS_X')
        s += 50 
    
def usrednen():
    kolich = menu_usredn.get()
    if kolich == '1':
        ser.write(b'9')
    elif kolich == '5':
        ser.write(b'A')
    elif kolich == '10':
        ser.write(b'B')
    elif kolich == '15':
        ser.write(b'C')
    elif kolich == '20':
        ser.write(b'D')
    elif kolich == '40':
        ser.write(b'E')

def zaderj():
    zaderjka_1 = menu_delay_1.get()
    zaderjka_2 = menu_delay_2.get()
    if zaderjka_1 == '50':
        ser.write(b'F')
    elif zaderjka_1 == '100':
        ser.write(b'G')
    elif zaderjka_1 == '150':
        ser.write(b'H')
    elif zaderjka_1 == '200':
        ser.write(b'I')

    if zaderjka_2 == '10':
        ser.write(b'J')
    elif zaderjka_2 == '15':
        ser.write(b'K')
    elif zaderjka_2 == '20':
        ser.write(b'L')
    elif zaderjka_2 == '30':
        ser.write(b'M')


btn_Znach = Button(root, text="Выбрать оси", command = osy)
btn_Znach.place(x = 20, y = 240)



# вывод ВАХ
btn_vivod = Button(root, text="Вывод", command = vivod)
btn_vivod.place(x = 20, y = 600)

btn_och = Button(root, text="Очистить", command = ochist)
btn_och.place(x = 80, y = 600)

btn_usred = Button(root, text="Выбрать", command = usrednen)
btn_usred.place(x = 20, y = 350)

btn_zaderj = Button(root, text="Задать", command = zaderj)
btn_zaderj.place(x = 20, y = 520)

root.mainloop()
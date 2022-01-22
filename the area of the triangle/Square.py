from tkinter import *
import math

root = Tk()
root.title("Area of ​​a triangle")
root.iconbitmap('icon.ico')
root.geometry("1320x640")
root.resizable(width=False, height=False)

# Поле графика
canvas = Canvas(root, width=1040, height=640, bg="white")
canvas.pack(side = "right")

frame = Frame(root)
frame.pack(pady = 135)

# Линии сетки по вертикали 
for y in range(21):
    k = 50 * y
    canvas.create_line(20+k, 620, 20+k, 20, width=1, fill="lightgrey")

# Линии сетки по горизотали 
for x in range(13):
    k = 50 * x
    canvas.create_line(20, 20+k, 1020, 20+k, width=1, fill="lightgrey")

# ось Y
canvas.create_line(520, 20, 520, 620, width=1, arrow=FIRST, fill="black")
# ocь X
canvas.create_line(20, 320, 1020, 320, width=1, arrow=LAST, fill="black")



# Надписи
label_tx = Label(root, text = "Расчет площади треугольника:", font="Arial 14" )   
label_tx.place(x = 0, y = 10)
label_A = Label(root, text = "Точка А(x,y): ", font="Arial 10")     #А
label_A.place(x = 0, y = 35)
label_B = Label(root, text = "Точка B(x,y): ", font="Arial 10")     #B
label_B.place(x = 0, y = 55)
label_C = Label(root, text = "Точка C(x,y): ", font="Arial 10")     #C
label_C.place(x = 0, y = 75)
label_tx = Label(root, text = "Маштаб сетки: ", font="Arial 14" )   
label_tx.place(x = 0, y = 100)
label_answ = Label(root, text = "Площадь ΔABC: ", font="Arial 14")  #Ответ
label_answ.place(x = 0, y = 250)

# Поля ввода
entry_Ax = Entry(root, width=15)
entry_Ax.place(x = 80, y = 37)
entry_Ay = Entry(root, width=15)
entry_Ay.place(x = 180, y = 37)

entry_Bx = Entry(root, width=15)
entry_Bx.place(x = 80, y = 57)
entry_By = Entry(root, width=15)
entry_By.place(x = 180, y = 57)

entry_Cx = Entry(root, width=15)
entry_Cx.place(x = 80, y = 77)
entry_Cy = Entry(root, width=15)
entry_Cy.place(x = 180, y = 77)

entry_answ = Entry(root, width=20)
entry_answ.place(x = 150, y = 255)



def func():
    global T
    if var.get() == 0:
        canvas.delete("ir")
        canvas.create_text(520, 10, text = "300", fill="black", tag = "ir")
        canvas.create_text(513, 330, text = "0", fill="black", tag = "ir")
        canvas.create_text(1030, 330, text = "500", fill="black", tag = "ir")
        T = 1
       
    elif var.get() == 1: 
        canvas.delete("ir")
        canvas.create_text(520, 10, text = "150", fill="black", tag = "ir")
        canvas.create_text(513, 330, text = "0", fill="black", tag = "ir")
        canvas.create_text(1030, 330, text = "250", fill="black", tag = "ir")
        T = 2

    elif var.get() == 2:
        canvas.delete("ir")
        canvas.create_text(520, 10, text = "6", fill="black", tag = "ir")
        canvas.create_text(513, 330, text = "0", fill="black", tag = "ir")
        canvas.create_text(1030, 330, text = "10", fill="black", tag = "ir")
        T = 50

  
      

var = IntVar()

big = Radiobutton(frame, text='50x50', width=5, height=1, indicatoron=0, variable=var, value=0, command = func)

sr = Radiobutton(frame, text='20x20', width=5, height=1, indicatoron=0, variable=var, value=1, command = func)

sm = Radiobutton(frame, text='1x1', width=5, height=1, indicatoron=0, variable=var, value=2, command = func)

# Функция построения треугольника 
def triangle(Ax, Ay, Bx, By, Cx, Cy):
    global linAB
    xyAB = []
    xyBC = []
    xyCA = []
    for x in range (int(entry_Ax.get())*T, int(entry_Bx.get())*T):
        y = -((By - Ay)*(x - Ax)/(Bx - Ax) + Ay)
        xyAB.append(x + 520)
        xyAB.append(y + 320)
    for x in range(int(entry_Bx.get())*T, int(entry_Cx.get())*T):
        y = -((Cy - By)*(x - Bx)/(Cx - Bx) + By)
        xyBC.append(x + 520)
        xyBC.append(y + 320)
    for x in range(int(entry_Ax.get())*T, int(entry_Cx.get())*T):
        y = -((Cy - Ay)*(x - Ax)/(Cx - Ax) + Ay)
        xyCA.append(x + 520)
        xyCA.append(y + 320)
    linAB = canvas.create_line(xyAB, xyBC, xyCA, fill="red")

# Функция расчета площади 
def square(Ax, Ay, Bx, By, Cx, Cy):
    S = ((Ax - Cx)*(By - Cy) - (Ay - Cy)*(Bx - Cx))/2
    text = S
    if S < 0:
        S = -S
        text = S
    return text
    
# Функция удаления и вставки площади
def inserter(value):
    entry_answ.delete(0, END)
    entry_answ.insert(END, str(value))

# Функция подстановки введенных данных в аравнение площади 
def handler():
    try:
        Ax_val = float(entry_Ax.get())
        Ay_val = float(entry_Ay.get())
        Bx_val = float(entry_Bx.get())
        By_val = float(entry_By.get())
        Cx_val = float(entry_Cx.get())
        Cy_val = float(entry_Cy.get())
        inserter(square(Ax_val, Ay_val, Bx_val, By_val, Cx_val, Cy_val))
    except ValueError:
        inserter("Введи значения")


# Кнопка
btn_calc = Button(root, text="Расчитать и построить", command = handler)
btn_calc.bind("<Button-1>", lambda event: triangle(float(entry_Ax.get())*T, float(entry_Ay.get())*T, float(entry_Bx.get())*T, float(entry_By.get())*T, float(entry_Cx.get())*T, float(entry_Cy.get())*T))
btn_calc.place(x = 68, y = 220)


big.pack(anchor=W)
sr.pack(anchor=W)
sm.pack(anchor=W)

root.mainloop()
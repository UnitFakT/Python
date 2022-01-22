import math 
from tkinter import *
from math import sqrt


root = Tk()
root.title("Quadratic roots")
root.geometry("320x400")
root.resizable(width=False, height=False)

frame = Frame(root)
frame.grid(pady = 65)

label_tx = Label(root, text = "Расчет корней квадратного уравнения:", font="Arial 13" )   
label_tx.place(x = 5, y = 5)

label_x2 = Label(root, text = "x^2 +", font="Arial 12" )   
label_x2.place(x = 45, y = 33)

label_x2 = Label(root, text = "x +", font="Arial 12" )   
label_x2.place(x = 125, y = 33)

label_x2 = Label(root, text = "= 0", font="Arial 12" )   
label_x2.place(x = 195, y = 33)

entry_a = Entry(root, width=5)
entry_a.place(x = 10, y = 37)

entry_b = Entry(root, width=5)
entry_b.place(x = 90, y = 37)

entry_c = Entry(root, width=5)
entry_c.place(x = 155, y = 37)

output = Text(frame, bg="white", font="Arial 10", width=45, height=5)
output.grid(row=2, columnspan=8)


def Quadratic_roots(a, b, c):
    D = b**2 - 4*a*c
    if D < 0:
        X1 = (-b + math.sqrt(-D)*complex(0,1))/(2*a)
        X2 = (-b - math.sqrt(-D)*complex(0,1))/(2*a)
        text = "Дискриминант равен: %s \n X1 равен: %s \n X2 равен: %s \n" % (D, X1, X2)
        return text
    else:
        X1 = (-b + math.sqrt(D))/(2*a)
        X2 = (-b - math.sqrt(D))/(2*a)
        text = "Дискриминант равен: %s \n X1 равен: %s \n X2 равен: %s \n" % (D, X1, X2)
        return text

def inserter(value):
    output.delete("0.0",END)
    output.insert(END,str(value))

def handler():
    try:
        a_val = float(entry_a.get())
        b_val = float(entry_b.get())
        c_val = float(entry_c.get())
        inserter(Quadratic_roots(a_val, b_val, c_val))
    except ValueError:
        inserter("Ощибка")

btn1_calc = Button(root, text="Расчитать", command=handler)
btn1_calc.place(x = 240, y = 33)

root.mainloop()


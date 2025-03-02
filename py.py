import tkinter
import time
from threading import Thread

def button_click():
    global running
    if running == True:
        running = False
    else:
        running = True

def window():
    top = tkinter.Tk()
    Button = tkinter.Button(top, text="Start", command=button_click).pack()
    top.mainloop()

running = False

t = Thread(target=window)
t.start()

for i in range(10):

    if running == False:
        while running == False:
            # ожидаем повторного нажатия кнопочки
            time.sleep(2)

    if running == True:
        # выполняем основную полезную работу программы
        print(i)
        time.sleep(1)
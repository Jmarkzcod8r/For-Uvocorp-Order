# import tkinter as tk
# import pyautogui as coordinates

# win = tk.Tk()
# win.geometry('200x50+550+250')
# win.title('Mos Loc')
# win.config(bg='#323232')
# # win.attributes('-topmos', 1)

# frame = tk.Frame()


# lab = tk.Label(text='')
# lab.pack()


# def update():
#     lab.configure(text='this are your ' +str( coordinates.position()))
    
#     frame.after(20, update)


# update()
# frame.mainloop()

# python3
import threading

import pyautogui, sys
print('Press Ctrl-C to quit.')
try:
    
    while True :
        x, y = pyautogui.position()
        positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
    
        while x > 300:
            
            print(positionStr, end='')
            print('\b' * len(positionStr), end='', flush=True)
        while x < 300:
            # x, y = pyautogui.position()
            # positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)

            def setInterval(func,time):
                e = threading.Event()
                while not e.wait(time):
                    func()
            def foo():
                print('you need to go back')
            setInterval(foo,5)

        # else:
            # def setInterval(func,time):
            #     e = threading.Event()
            #     while not e.wait(time):
            #         func()
            # def foo():
            #     print('you need to go back')
            # setInterval(foo,5)
except KeyboardInterrupt:
    print('\n')
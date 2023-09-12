from tkinter import *
from tkinter import ttk

root = Tk()
root.title('INTEGRAÇÃO FOODY - ROBO')

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)



if __name__ == '__main__':
    root.mainloop()
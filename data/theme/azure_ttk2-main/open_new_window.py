import tkinter as tk


def new_window1():
    " new window"
    try:
        if win1.state() == "normal": win1.focus()
    except NameError as e:
        print(e)
        win1 = tk.Toplevel()
        win1.geometry("300x300+500+200")
        win1["bg"] = "navy"
        lb = tk.Label(win1, text="Hello")
        lb.pack()


win = tk.Tk()
win.geometry("200x200+200+100")
button = tk.Button(win, text="Open new Window")
button['command'] = new_window1
button.pack()
win.mainloop()